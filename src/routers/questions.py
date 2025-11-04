from flask import Blueprint, request, jsonify
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.dtos.questions import PollCreateRequest, PollResponse
from src.dtos.questions import PollOptionCreateRequest
from src.models import Poll, PollOption
from src.core.db import db

questions_bp = Blueprint("questions", __name__, url_prefix='/questions')


# CRUD (Questions)

# R
def list_of_questions():
    polls = db.session.query(Poll).all()
    result = [
        {
            "id": p.id,
            "title": p.title,
            "category": {"id": p.category.id, "name": p.category.name}
        }
        for p in polls
    ]
    return jsonify(result), 200


# C
@questions_bp.route('/create', methods=["POST"])
def create_new_question():
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify(
                {
                    "error": "Validation Error",
                    "message": "Сырых данных не обнаружено"
                }
            ), 400  # BAD REQUEST

        poll_data = PollCreateRequest.model_validate(raw_data)

        category_id = getattr(poll_data, "category_id", None)
        if not category_id:
            return jsonify(
                {"error": "Validation Error", "message": "category_id обязателен"}
            ), 400

        from src.models import Category
        category = db.session.get(Category, category_id)
        if not category:
            return jsonify(
                {"error": "Not Found", "message": f"Категория с id={category_id} не найдена"}
            ), 404

        options_data = poll_data.options
        poll_dict: dict[str, Any] = poll_data.model_dump(exclude={'options'})
        poll: Poll = Poll(**poll_dict)

        poll.category = category

        db.session.add(poll)
        db.session.flush()

        for opt in options_data:  # type: PollOptionCreateRequest
            option: PollOption = PollOption(
                poll_id=poll.id,
                text=opt.text
            )
            poll.options.append(option)

        db.session.commit()
        db.session.refresh(poll)

        poll_response: dict[str, Any] = (
            PollResponse
            .model_validate(poll)
            .model_dump()
        )

        return jsonify(poll_response), 201

    except ValidationError as exc:
        return jsonify(
            {
                "error": "Validation Error",
                "message": exc.errors()
            }
        ), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify(
            {
                "error": "DATABASE Error",
                "message": str(exc)
            }
        ), 400
    except Exception as exc:
        return jsonify(
            {
                "error": "Unexpected Error",
                "message": str(exc)
            }
        ), 500


# R
@questions_bp.route('/<int:question_id>', methods=["GET"])
def get_question_by_id(question_id: int) -> dict[str, Any]:
    return {
        "id": question_id,
        "title": "На сколько вы в шоке?"
    }


# U
@questions_bp.route('/<int:question_id>/update', methods=["PUT", "PATCH"])
def update_question(question_id: int) -> str:
    return f"Question with ID {question_id} was updated. Congrats!"


# D
@questions_bp.route('/<int:question_id>/delete', methods=["DELETE"])
def delete_question(question_id: int) -> str:
    return f"Question with ID {question_id} was deleted successfully. Congrats!"