from rest_framework.authtoken.models import Token

from dongtai_common.models.department import Department


def update_department_data():
    department_dict = {}
    departments = Department.objects.order_by("id").all()
    for department in departments:
        if department.parent_id == -1:
            department_dict[department.id] = f"{department.id}"
        else:
            department_dict[department.id] = f"{department_dict[department.parent_id]}-{department.id}"
        department.department_path = department_dict[department.id]
        department.token = Token().generate_key()
        department.save()
