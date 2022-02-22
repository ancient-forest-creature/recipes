from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import math
from datetime import datetime

class Recipe:
    def __init__(self , data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.made_on = data['made_on']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def time_from(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_recipes_by_sender(cls, data):
        query = "SELECT * FROM recipes WHERE sender_id = %(sender_id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        print(results)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        res = connectToMySQL('recipes_schema').query_db(query, data)
        if len(res) < 1:
            return False
        result = cls(res[0])
        return result

    @classmethod
    def get_recipe_by_owner(cls, data):
        data = {'id':data}
        # query = "SELECT * FROM recipe WHERE owner_id = %(owner_id)s;"
        query = "SELECT users.first_name as user, recipes.* FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s"
        res = connectToMySQL('recipes_schema').query_db(query, data)
        print("res is :")
        print(res[0]['name'])
        # if len(res) < 1:
        #     return False
        messages = []
        for message in res:
            if res[0]['name'] == None:
                print('hit')
                return
            messages.append(cls(message))
        return messages

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, made_on, under_30, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(made_on)s, %(under_30)s, %(user_id)s);"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, made_on=%(made_on)s, under_30=%(under_30)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def delete_recipe(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @staticmethod
    def validate_recipe(msg):
        is_valid = True
        if len(msg["name"]) < 3:
            flash("name is too short. Must be at least 3 characters", "send_msg")
            is_valid=False
        if len(msg["description"]) < 3:
            flash("description is too short. Must be at least 3 characters", "send_msg")
            is_valid=False
        if len(msg["instruction"]) < 3:
            flash("instruction is too short. Must be at least 3 characters", "send_msg")
            is_valid=False
        return is_valid