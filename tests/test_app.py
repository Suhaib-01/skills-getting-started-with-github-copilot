def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Basketball" in data
    assert data["Basketball"]["max_participants"] == 15


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    r = client.post(f"/activities/Basketball/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    r2 = client.get("/activities")
    assert email in r2.json()["Basketball"]["participants"]


def test_signup_duplicate(client):
    # Attempt to sign up an existing participant
    current = client.get("/activities").json()["Basketball"]["participants"][0]
    r = client.post(f"/activities/Basketball/signup?email={current}")
    assert r.status_code == 400


def test_unregister_success(client):
    email = "temp@mergington.edu"
    # Sign up then unregister
    r = client.post(f"/activities/Tennis/signup?email={email}")
    assert r.status_code == 200

    r2 = client.delete(f"/activities/Tennis/unregister?email={email}")
    assert r2.status_code == 200
    assert "Unregistered" in r2.json().get("message", "")

    r3 = client.get("/activities")
    assert email not in r3.json()["Tennis"]["participants"]


def test_unregister_not_registered(client):
    r = client.delete("/activities/Tennis/unregister?email=not@there.com")
    assert r.status_code == 400


def test_activity_not_found(client):
    r = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert r.status_code == 404

    r2 = client.delete("/activities/NoSuchActivity/unregister?email=a@b.com")
    assert r2.status_code == 404
