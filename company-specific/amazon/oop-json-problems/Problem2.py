# create classes User, Role, Resource, AccessControlList
# load each from json file and create objects
# method to create -> can_access (whether they can or not)

import json

class User:
    def __init__(self, user_id, roles=None):
        self.user_id = user_id
        self.roles = roles

class AccessControlList():
    def __init__(self):
        self.users = {} # {user_id: roles}
        self.roles = {} # {role name: set of permissions}
        self.resources = {} # {resource_id: resource}
    
    def loadSystem(self, path):
        with open(path) as file:
            jsonObj = json.load(file)
            # manage roles
            if not jsonObj.get('roles') or not jsonObj.get('users') or not jsonObj.get('resources'):
                raise ValueError("Missing fields for initialization")
            for role in jsonObj['roles']:
                name = role['name']
                permissions = role['permissions']
                if not name:
                    raise ValueError("Missing role name")
                elif not permissions:
                    raise ValueError("Missing role permissions")
                self.roles[name] = {}
                for type, actions in permissions.items():
                    self.roles[name][type] = set(actions)
            
            for res in jsonObj['resources']:
                res_id = res['resource_id']
                res_type = res['type']
                if not res_id:
                    raise ValueError("Missing Resource Identifier")
                elif not res_type:
                    raise ValueError("Missing resource type")
                self.resources[res_id] = res_type
            
            for user in jsonObj['users']:
                u_id = user['user_id']
                u_roles = user['roles']
                if not u_id:
                    raise ValueError("Missing User ID")
                self.users[u_id] = u_roles
    
    def can_access(self, user_id, resource_id, action) -> bool:
        if user_id not in self.users:
            raise ValueError(f"User {user_id} does not exist.")
        elif resource_id not in self.resources:
            raise ValueError(f"Resource {resource_id} does not exist.")
        resource_type = self.resources[resource_id]
        for role in self.users[user_id]:
            if role in self.roles:
                all_perms = self.roles[role]
                if resource_type in all_perms:
                        if action in all_perms[type]: # search in set of actions for type of permission
                            return True
        return False
    