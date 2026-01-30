def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    email = "testuser@example.com"
    # Successful signup
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json().get("message") == f"Signed up {email} for Chess Club"

    # Participant now present
    resp2 = client.get("/activities")
    assert email in resp2.json()["Chess Club"]["participants"]

    # Duplicate signup fails
    resp3 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp3.status_code == 400


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404


def test_unregister(client):
    email = "michael@mergington.edu"
    # Ensure present initially
    resp = client.get("/activities")
    assert email in resp.json()["Chess Club"]["participants"]

    # Unregister
    resp2 = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp2.status_code == 200
    assert resp2.json().get("message") == f"Unregistered {email} from Chess Club"

    # Now client shows absent
    resp3 = client.get("/activities")
    assert email not in resp3.json()["Chess Club"]["participants"]

    # Trying to unregister again returns 400
    resp4 = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp4.status_code == 400


def test_unregister_nonexistent_activity(client):
    resp = client.delete("/activities/NotHere/participants?email=a@b.com")
    assert resp.status_code == 404
