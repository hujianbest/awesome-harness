from bootstrap.runtime_home_doctor import RuntimeHomeDoctor


def test_runtime_home_doctor_reports_ok_for_valid_layout():
    doctor = RuntimeHomeDoctor()
    report = doctor.check("D:/Garage/.garage", has_workspace=True)
    assert report["status"] == "ok"


def test_runtime_home_doctor_reports_missing_workspace():
    doctor = RuntimeHomeDoctor()
    report = doctor.check("D:/Garage/.garage", has_workspace=False)
    assert report["status"] == "warn"
    assert report["issue"] == "workspace_missing"
