from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location(
        "websocket_load_balancer_solution",
        Path(__file__).parents[1] / "solution.py",
    )
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


routeRequests = _load().routeRequests


def test_part_1_routes_to_least_loaded_target_and_breaks_ties_by_index():
    requests = [
        "CONNECT,c1,u1,a",
        "CONNECT,c2,u2,b",
        "CONNECT,c3,u3,c",
        "CONNECT,c4,u4,d",
    ]
    assert routeRequests(3, 10, requests) == [
        "c1,u1,1",
        "c2,u2,2",
        "c3,u3,3",
        "c4,u4,1",
    ]


def test_part_1_single_target_receives_every_connection():
    requests = ["CONNECT,a,u1,x", "CONNECT,b,u2,y"]
    assert routeRequests(1, 10, requests) == ["a,u1,1", "b,u2,1"]


def test_part_1_routing_is_sequential_not_precomputed():
    requests = [
        "CONNECT,z,u1,o1",
        "CONNECT,a,u2,o2",
        "CONNECT,m,u3,o3",
    ]
    assert routeRequests(2, 10, requests) == [
        "z,u1,1",
        "a,u2,2",
        "m,u3,1",
    ]


def test_part_2_disconnect_frees_load_before_next_route():
    requests = [
        "CONNECT,c1,u1,a",
        "CONNECT,c2,u2,b",
        "CONNECT,c3,u3,c",
        "DISCONNECT,c1,u1,a",
        "CONNECT,c4,u4,d",
    ]
    assert routeRequests(2, 10, requests) == [
        "c1,u1,1",
        "c2,u2,2",
        "c3,u3,1",
        "c4,u4,1",
    ]


def test_part_2_disconnect_of_missing_id_is_no_op():
    requests = [
        "DISCONNECT,missing,u,x",
        "CONNECT,a,u1,x",
    ]
    assert routeRequests(2, 10, requests) == ["a,u1,1"]


def test_part_2_disconnect_uses_connection_id_not_supplied_metadata():
    requests = [
        "CONNECT,a,original_user,original_object",
        "DISCONNECT,a,different_user,different_object",
        "CONNECT,b,u2,next_object",
    ]
    assert routeRequests(2, 10, requests) == [
        "a,original_user,1",
        "b,u2,1",
    ]


def test_part_2_disconnected_id_can_connect_again_with_new_metadata():
    requests = [
        "CONNECT,same,old_user,old_object",
        "DISCONNECT,same,old_user,old_object",
        "CONNECT,same,new_user,new_object",
    ]
    assert routeRequests(2, 10, requests) == [
        "same,old_user,1",
        "same,new_user,1",
    ]


def test_part_3_active_object_affinity_overrides_lower_load_target():
    requests = [
        "CONNECT,a,u1,shared",
        "CONNECT,b,u2,other",
        "CONNECT,c,u3,shared",
    ]
    assert routeRequests(3, 10, requests) == [
        "a,u1,1",
        "b,u2,2",
        "c,u3,1",
    ]


def test_part_3_affinity_remains_until_last_object_connection_disconnects():
    requests = [
        "CONNECT,a,u1,shared",
        "CONNECT,b,u2,shared",
        "DISCONNECT,a,u1,shared",
        "CONNECT,c,u3,other",
        "CONNECT,d,u4,shared",
    ]
    assert routeRequests(3, 10, requests) == [
        "a,u1,1",
        "b,u2,1",
        "c,u3,2",
        "d,u4,1",
    ]


def test_part_3_affinity_clears_after_last_connection_disconnects():
    requests = [
        "CONNECT,a,u1,shared",
        "DISCONNECT,a,u1,shared",
        "CONNECT,filler,u2,other",
        "CONNECT,b,u3,shared",
    ]
    assert routeRequests(2, 10, requests) == [
        "a,u1,1",
        "filler,u2,1",
        "b,u3,2",
    ]


def test_part_3_affinities_for_different_objects_are_independent():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,b,u2,y",
        "CONNECT,c,u3,y",
        "CONNECT,d,u4,x",
    ]
    assert routeRequests(2, 10, requests) == [
        "a,u1,1",
        "b,u2,2",
        "c,u3,2",
        "d,u4,1",
    ]


def test_part_4_first_complete_example_covers_capacity_and_affinity():
    requests = [
        "CONNECT,c1,u1,docA",
        "CONNECT,c2,u2,docB",
        "CONNECT,c3,u3,docA",
        "DISCONNECT,c1,u1,docA",
        "CONNECT,c4,u4,docC",
        "CONNECT,c5,u5,docA",
        "CONNECT,c6,u6,docA",
    ]
    assert routeRequests(3, 2, requests) == [
        "c1,u1,1",
        "c2,u2,2",
        "c3,u3,1",
        "c4,u4,3",
        "c5,u5,1",
    ]


def test_part_4_connection_is_rejected_when_every_target_is_full():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,b,u2,y",
        "CONNECT,c,u3,z",
    ]
    assert routeRequests(2, 1, requests) == ["a,u1,1", "b,u2,2"]


def test_part_4_full_affinity_target_rejects_without_fallback():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,b,u2,x",
    ]
    assert routeRequests(3, 1, requests) == ["a,u1,1"]


def test_part_4_duplicate_active_id_replays_original_log_and_metadata():
    requests = [
        "CONNECT,same,original,x",
        "CONNECT,same,replacement,y",
        "CONNECT,new,new_user,y",
    ]
    assert routeRequests(2, 1, requests) == [
        "same,original,1",
        "same,original,1",
        "new,new_user,2",
    ]


def test_part_4_duplicate_active_id_does_not_increase_load():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,a,ignored,ignored_object",
        "CONNECT,b,u2,y",
        "CONNECT,c,u3,z",
    ]
    assert routeRequests(2, 2, requests) == [
        "a,u1,1",
        "a,u1,1",
        "b,u2,2",
        "c,u3,1",
    ]


def test_part_4_duplicate_active_id_logs_even_when_target_is_full():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,a,u2,y",
    ]
    assert routeRequests(1, 1, requests) == ["a,u1,1", "a,u1,1"]


def test_part_4_rejected_connection_id_and_object_are_not_reserved():
    requests = [
        "CONNECT,occupant,u1,occupied",
        "CONNECT,retry,u2,new_object",
        "DISCONNECT,occupant,u1,occupied",
        "CONNECT,retry,u3,new_object",
    ]
    assert routeRequests(1, 1, requests) == [
        "occupant,u1,1",
        "retry,u3,1",
    ]


def test_part_5_second_complete_example_removes_all_before_sorted_reroute():
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
    assert routeRequests(3, 2, requests) == [
        "a,u1,1",
        "b,u2,2",
        "c,u3,1",
        "d,u4,3",
        "a,u1,2",
        "f,u6,1",
    ]


def test_part_5_third_complete_example_restores_target_after_rerouting():
    requests = [
        "CONNECT,conn1,userA,obj1",
        "CONNECT,conn2,userB,obj2",
        "SHUTDOWN,1",
        "CONNECT,conn3,userC,obj3",
    ]
    assert routeRequests(2, 10, requests) == [
        "conn1,userA,1",
        "conn2,userB,2",
        "conn1,userA,2",
        "conn3,userC,1",
    ]


def test_part_5_duplicate_after_reroute_replays_current_assignment():
    requests = [
        "CONNECT,a,original_user,x",
        "CONNECT,b,u2,y",
        "SHUTDOWN,1",
        "CONNECT,a,replacement_user,replacement_object",
    ]
    assert routeRequests(2, 10, requests) == [
        "a,original_user,1",
        "b,u2,2",
        "a,original_user,2",
        "a,original_user,2",
    ]


def test_part_5_evictions_are_rerouted_in_lexicographic_id_order():
    requests = [
        "CONNECT,c2,u2,shared",
        "CONNECT,c10,u10,shared",
        "SHUTDOWN,1",
    ]
    assert routeRequests(2, 10, requests) == [
        "c2,u2,1",
        "c10,u10,1",
        "c10,u10,2",
        "c2,u2,2",
    ]


def test_part_5_reroutes_update_load_sequentially():
    requests = [
        "CONNECT,a,u1,shared",
        "CONNECT,b,u2,shared",
        "CONNECT,c,u3,other",
        "CONNECT,d,u4,third",
        "SHUTDOWN,1",
    ]
    assert routeRequests(3, 10, requests) == [
        "a,u1,1",
        "b,u2,1",
        "c,u3,2",
        "d,u4,3",
        "a,u1,2",
        "b,u2,2",
    ]


def test_part_5_unplaceable_reroute_is_dropped_without_log():
    requests = [
        "CONNECT,a,u1,x",
        "CONNECT,b,u2,y",
        "CONNECT,c,u3,x",
        "SHUTDOWN,1",
    ]
    assert routeRequests(2, 1, requests) == [
        "a,u1,1",
        "b,u2,2",
    ]


def test_part_5_all_dropped_object_connections_leave_no_stale_affinity():
    requests = [
        "CONNECT,a,u1,shared",
        "CONNECT,blocker1,u2,blocked",
        "CONNECT,b,u3,shared",
        "CONNECT,blocker2,u4,blocked",
        "SHUTDOWN,1",
        "CONNECT,new,u5,shared",
    ]
    assert routeRequests(2, 2, requests) == [
        "a,u1,1",
        "blocker1,u2,2",
        "b,u3,1",
        "blocker2,u4,2",
        "new,u5,1",
    ]


def test_part_5_dropped_eviction_id_can_connect_later_as_new():
    requests = [
        "CONNECT,same,old_user,old_object",
        "SHUTDOWN,1",
        "CONNECT,same,new_user,new_object",
    ]
    assert routeRequests(1, 1, requests) == [
        "same,old_user,1",
        "same,new_user,1",
    ]


def test_part_5_shutdown_of_empty_target_emits_nothing_and_restores_it():
    requests = [
        "SHUTDOWN,1",
        "CONNECT,a,u1,x",
    ]
    assert routeRequests(2, 10, requests) == ["a,u1,1"]


def test_part_5_repeated_shutdown_of_same_target_is_a_new_event():
    requests = [
        "CONNECT,a,u1,x",
        "SHUTDOWN,1",
        "CONNECT,c,u3,z",
        "SHUTDOWN,1",
    ]
    assert routeRequests(2, 10, requests) == [
        "a,u1,1",
        "a,u1,2",
        "c,u3,1",
        "c,u3,2",
    ]


def test_part_5_reroute_rebuilds_affinity_in_sorted_order():
    requests = [
        "CONNECT,z,u1,shared",
        "CONNECT,a,u2,shared",
        "CONNECT,other,u3,different",
        "SHUTDOWN,1",
    ]
    assert routeRequests(2, 3, requests) == [
        "z,u1,1",
        "a,u2,1",
        "other,u3,2",
        "a,u2,2",
        "z,u1,2",
    ]
