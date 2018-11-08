from api.models import db, Users

# client passed from client - look into pytest for more info about fixtures
# test client api: http://flask.pocoo.org/docs/1.0/api/#test-client
def test_index(client):
    rs = client.get("/")
    assert rs.status_code == 200


def test_get_person(client):
    rs = client.get("/users")

    assert rs.status_code == 200
    ret_dict = rs.json  # gives you a dictionary
    assert ret_dict["success"] == True
    assert ret_dict["result"]["users"] == []

    # create Person and test whether it returns a person
    temp_person = Users(email="tim@gmail.com",username="Tim",password="Tim1")
    db.session.add(temp_person)
    db.session.commit()

    rs = client.get("/users")
    ret_dict = rs.json
    assert len(ret_dict["result"]["users"]) == 1
    assert ret_dict["result"]["users"][0] == {'_id': 1,'email': 'tim@gmail.com','is_active': True,'password': 'Tim1','username': 'Tim'}
