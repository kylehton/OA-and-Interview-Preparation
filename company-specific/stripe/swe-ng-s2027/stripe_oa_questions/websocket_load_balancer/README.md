# WebSocket Load Balancer — Parts 1–5

**Company:** Stripe  
**Difficulty:** Hard  
**Stage:** Intern, New Grad OA and Onsite Interview  
**Last reported:** September 16, 2026

## Problem statement

Source note: About 95% of the judged core rules follow the complete available
question photos and detailed report, including active-object affinity, capacity
rejection, successful reroute logs, ID-sorted eviction processing, and restoring
the target afterward. A shorter recurrence describes sequential routing and
continued unavailability after eviction; this practice selects the more fully
specified least-load and temporary-shutdown contract. Duplicate active IDs
retain their original assignment and log as described by that recurrence.
Missing-disconnect no-ops, numeric and aggregate-work bounds, the ASCII
connection/user-ID domains, and output-size bounds are authored practice
choices.

Stripe runs multiple Jupyter targets and routes long-lived WebSocket
connections across them. Implement `routeRequests` and process the request
stream in order. Targets use one-based indices from `1` through `numTargets`.

## Request records

```text
CONNECT,connectionId,userId,objectId
DISCONNECT,connectionId,userId,objectId
SHUTDOWN,targetIndex
```

Every successful assignment appends this record to the returned log:

```text
connectionId,userId,targetIndex
```

Rejected connections and actions that do not assign a connection append
nothing.

## Part 1: Least-loaded routing

A new connection without an active object affinity goes to the active target
with the fewest connections. Break a load tie by smaller target index.

## Part 2: Disconnect

`DISCONNECT` removes the active connection with that ID and frees its target
slot. A disconnect for a non-active ID is a no-op.

## Part 3: Object affinity

While an object has active connections, every later connection for that
`objectId` must use the same target. When the last active connection for an
object disappears, its affinity is cleared.

## Part 4: Capacity and duplicate IDs

No target may exceed `maxConnectionsPerTarget`. If the target selected by the
preceding rules is full, reject the connection without trying another target.

If a `CONNECT` repeats an active `connectionId`, keep state unchanged and append
that connection's original user and target log.

## Part 5: Shutdown and rerouting

`SHUTDOWN,targetIndex` temporarily excludes that target from routing.

First remove all of its active connections and clear their old state, including
any object affinity whose last connection was removed. Then reroute the evicted
connections in ascending lexicographic `connectionId` order using Parts 1–4.
The shutting-down target remains ineligible throughout this rerouting.

Each successful reroute appends a new log. An unplaceable connection is dropped
without a log. After all evictions are processed, the target becomes available
again for future requests. A later shutdown of the same target is processed as
a new event.

## Function

FastPrep signature:

```text
routeRequests(numTargets: int, maxConnectionsPerTarget: int, requests: String[]) → String[]
```

Python workspace signature:

```python
def routeRequests(
    numTargets: int,
    maxConnectionsPerTarget: int,
    requests: list[str],
) -> list[str]:
    ...
```

## Examples

### Example 1

```python
numTargets = 3
maxConnectionsPerTarget = 2
requests = [
    "CONNECT,c1,u1,docA",
    "CONNECT,c2,u2,docB",
    "CONNECT,c3,u3,docA",
    "DISCONNECT,c1,u1,docA",
    "CONNECT,c4,u4,docC",
    "CONNECT,c5,u5,docA",
    "CONNECT,c6,u6,docA",
]

routeRequests(numTargets, maxConnectionsPerTarget, requests)
# [
#     "c1,u1,1",
#     "c2,u2,2",
#     "c3,u3,1",
#     "c4,u4,3",
#     "c5,u5,1",
# ]
```

The second `docA` connection follows object affinity to target 1. Disconnecting
`c1` frees one slot there. The final `docA` connection is rejected because its
affinity target is full, so it produces no log.

### Example 2

```python
numTargets = 3
maxConnectionsPerTarget = 2
requests = [
    "CONNECT,a,u1,x",
    "CONNECT,b,u2,y",
    "CONNECT,c,u3,x",
    "CONNECT,d,u4,z",
    "SHUTDOWN,1",
    "CONNECT,e,u5,x",
    "DISCONNECT,b,u2,y",
    "CONNECT,f,u6,y",
]

routeRequests(numTargets, maxConnectionsPerTarget, requests)
# [
#     "a,u1,1",
#     "b,u2,2",
#     "c,u3,1",
#     "d,u4,3",
#     "a,u1,2",
#     "f,u6,1",
# ]
```

Shutdown removes both old connections before rerouting `a` and then `c`. The
first joins target 2; the second is dropped because object `x` is then pinned to
that full target. Target 1 becomes available again when shutdown finishes.
After `b` disconnects, the new object `y` connection `f` chooses the empty
target 1.

### Example 3

```python
numTargets = 2
maxConnectionsPerTarget = 10
requests = [
    "CONNECT,conn1,userA,obj1",
    "CONNECT,conn2,userB,obj2",
    "SHUTDOWN,1",
    "CONNECT,conn3,userC,obj3",
]

routeRequests(numTargets, maxConnectionsPerTarget, requests)
# [
#     "conn1,userA,1",
#     "conn2,userB,2",
#     "conn1,userA,2",
#     "conn3,userC,1",
# ]
```

`conn1` reroutes to target 2 while target 1 is temporarily unavailable. Target
1 reopens afterward, so `conn3` selects its zero load. The source example uses
an unspecified large capacity; 10 is the practice value.

## Constraints

- `1 <= numTargets <= 10^5`.
- `1 <= maxConnectionsPerTarget <= 10^9`.
- `1 <= requests.length <= 2 * 10^5`.
- Every record follows one documented schema.
- Identifiers are non-empty and contain no commas.
- Connection IDs and user IDs contain only ASCII letters, digits, underscores,
  or hyphens; object IDs are opaque strings.
- A `SHUTDOWN` target index is within `1..numTargets`.
- Each repeated shutdown performs the temporary eviction-and-reroute operation.
- The number of requests plus the total number of evicted connections processed
  across all shutdowns is at most `2 * 10^5`.
- The returned log contains at most 2048 entries, with at most 50000 ASCII
  characters in total across the entries, counting identifiers, commas, and
  target indices.
- Output order follows successful assignments, including duplicate-ID log
  repeats and sorted shutdown reroutes.

## Deterministic identity and lifecycle interpretation used by the tests

Connection identity is determined only by `connectionId`. The `userId` and
`objectId` fields supplied on `DISCONNECT` do not need to match the original
connection; if that connection ID is active, remove its stored connection and
its stored object membership.

For a duplicate active `CONNECT`, append the stored connection's original
`connectionId,userId,targetIndex` record. Ignore the duplicate request's new
user and object values, do not add load, and do not create or change affinity.
Once an ID becomes inactive through disconnect, shutdown eviction, or a failed
reroute, a later `CONNECT` with that ID is a new connection using the later
request's user and object.

A shutdown removes every evicted connection before the first reroute attempt.
Reroutes are then ordinary new assignments using each evicted connection's
stored user and object, except that the shutting-down target is temporarily
ineligible. The output bounds are input guarantees; do not truncate otherwise
valid assignment logs.

