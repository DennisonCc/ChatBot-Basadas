from app.domain.models import Employee, PauseRecord

def test_employee_model():
    emp = Employee(id="123", name="Test User", role="Admin")
    assert emp.id == "123"
    assert emp.name == "Test User"
    assert emp.role == "Admin"

def test_pause_record_model():
    pause = PauseRecord(
        id=1,
        tipo="ALMUERZO",
        empleado_id="123",
        empleado_nombre="Test User",
        fecha="2024-01-01",
        hora_inicio="12:00"
    )
    assert pause.tipo == "ALMUERZO"
    assert pause.hora_fin is None
