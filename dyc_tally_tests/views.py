import json
from typing import Optional, Tuple, List
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import TestType, TestQuestion, TestOption, TestResponse, TestAttempt

data_section = {}
fields_section = []
options_section = []
personal_data = []


def extract_payload_sections(
    payload: dict,
) -> Tuple[Optional[dict], List[dict], List[dict], List[dict]]:
    data_section = payload.get("data")
    fields_section = data_section.get("fields", []) if data_section else []
    options_section = []
    personal_data = []

    for field in fields_section:
        field_type = field.get("type").strip().upper()

        if field_type == "MULTIPLE_CHOICE":
            options_section.extend(field.get("options", []))
        elif field_type in ["INPUT_TEXT", "INPUT_EMAIL", "INPUT_PHONE_NUMBER"]:
            personal_data.append(field)
    return data_section, fields_section, options_section, personal_data


def get_type_of_dyc_test(data_section: dict) -> Optional[TestType]:
    form_id = data_section.get("formId")
    if not form_id:
        return None
    try:

        return TestType.objects.get(form_id=form_id)
    except ObjectDoesNotExist:
        return None
    return "", ""


def fill_test_question_model(fields_section, test_type_obj):

    for field in fields_section:
        question_text = field.get("label", "")
        question_key = field.get("key", "")

        obj, created = TestQuestion.objects.update_or_create(
            question_key=question_key,
            defaults={
                "question": question_text,
                "test_type": test_type_obj,
            },
        )
        print(f"{'Creado' if created else 'Actualizado'}: {obj.question}")


WEIGHING_MAP = {
    "Muy a menudo": 4,
    "A menudo": 3,
    "A veces": 2,
    "Rara vez": 1,
    "Nunca": 0,
    "Preescolar": 0,
    "Primaria": 0,
    "Secundaria": 0,
    "Nivel medio": 0,
    "Superior": 0,
}


def populate_test_options(fields_section, options_section):
    for field in fields_section:
        question_key = field.get("key", "")
        options = field.get("options", [])
        try:
            test_question = TestQuestion.objects.get(question_key=question_key)
        except TestQuestion.DoesNotExist:
            print(f" Pregunta no encontrada para key: {question_key}")
            continue
        for opt in options:
            option_id = opt.get("id", "")
            name_text = opt.get("text", "")
            weighing = WEIGHING_MAP.get(name_text, 0)
            obj, created = TestOption.objects.update_or_create(
                option_id=option_id,
                test_question=test_question,
                defaults={
                    "name_text": name_text,
                    "weighing": weighing,
                },
            )
            print(
                f"{'Creada' if created else 'Actualizada'} opción '{obj.name_text}' con ponderación {obj.weighing}"
            )


def save_test_attempt(personal_data) -> TestAttempt:
    first_name = None
    last_name = None
    email = None
    phone = None
    for field in personal_data:
        label = field.get("label", "").strip().lower()
        value = field.get("value", "").strip()
        field_type = field.get("type", "")
        if "nombre" == label:
            first_name = value
        if "apellido" == label:
            last_name = value
        if field_type == "INPUT_EMAIL" or "correo electrónico" in label:
            email = value
        if field_type == "INPUT_PHONE_NUMBER" or "teléfono" in label:
            print("EUREKA ENTRO ==> ", value)
            phone = value
        attempt = TestAttempt.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        print(f"TestAttempt creado: {attempt}")
    return attempt


def save_test_responses(fields_section, options_section, attempt: TestAttempt):
    question_map = {q.question_key: q for q in TestQuestion.objects.all()}
    option_map = {o.option_id: o for o in TestOption.objects.all()}
    payload_option_map = {opt.get("id"): opt for opt in options_section}
    total_score = 0
    education = ""
    for field in fields_section:
        if field.get("type") != "MULTIPLE_CHOICE":
            continue  # Sólo procesa preguntas de opción multiple

        question_key = field.get("key")
        question_obj = question_map.get(question_key)

        if not question_obj:
            print(f"Pregunta no encontrada para key {question_key}")
            continue

        selected_values = field.get("value")
        if not isinstance(selected_values, list):
            selected_values = [selected_values]

        for selected_option_id in filter(None, selected_values):
            option_obj = option_map.get(selected_option_id)

            if option_obj and option_obj.name_text:
                answer_text = option_obj.name_text
            else:
                payload_opt = payload_option_map.get(selected_option_id)
                answer_text = payload_opt.get("text") if payload_opt else None

            TestResponse.objects.create(
                attempt=attempt,
                question=question_obj,
                option=option_obj,
                answer_text=answer_text,
            )
            if option_obj:
                if option_obj.name_text in [
                    "Preescolar",
                    "Primaria",
                    "Secundaria",
                    "Nivel medio",
                    "Superior",
                ]:
                    print("OPTION_OBJ -> ", option_obj.name_text)
                    education = option_obj.name_text
                total_score += option_obj.weighing
    attempt.total_score = total_score
    attempt.education = education
    attempt.save(update_fields=["total_score", "education"])


@csrf_exempt
@require_POST
def dyc_test_tally_view(request):
    payload_from_tally = json.loads(request.body)
    data_section, fields_section, options_section, personal_data = (
        extract_payload_sections(payload_from_tally)
    )
    # Sección de datos del Payload de Tally
    payload_from_tally.get("data", {})
    test_type = get_type_of_dyc_test(data_section)
    fill_test_question_model(fields_section, test_type)
    populate_test_options(fields_section, options_section)
    test_aplicado = save_test_attempt(personal_data)
    save_test_responses(fields_section, options_section, test_aplicado)
    print("TEST aplicado --> ", test_aplicado)
    # populate_test_responses(payload_from_tally)
    if test_type:
        print("FORM NAME ", test_type.form_name)
        return JsonResponse({"Ok": "Payload recibido correctamente"}, status=200)

    return JsonResponse(
        {"error": f"Tipo de test {test_type.form_name} no encontrado"}, status=404
    )
