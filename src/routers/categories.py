from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.models.category import Category
from src.core.db import db
from src.schemas.question import CategoryBase

categories_bp = Blueprint("categories", __name__, url_prefix='/categories')


@categories_bp.route('', methods=["POST"])
def create_category():
    try:
        raw_data = request.get_json()
        if not raw_data:
            return jsonify({"error": "Validation Error", "message": "No input data"}), 400

        category_data = CategoryBase.model_validate(raw_data)
        category = Category(name=category_data.name)

        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)

        return jsonify(CategoryBase.model_validate(category).model_dump()), 201

    except ValidationError as exc:
        return jsonify({"error": "Validation Error", "message": exc.errors()}), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": str(exc)}), 400


@categories_bp.route('', methods=["GET"])
def get_all_categories():
    categories = db.session.query(Category).all()
    result = [CategoryBase.model_validate(c).model_dump() for c in categories]
    return jsonify(result), 200


@categories_bp.route('/<int:id>', methods=["PUT"])
def update_category(id):
    try:
        raw_data = request.get_json()
        if not raw_data:
            return jsonify({"error": "Validation Error", "message": "No input data"}), 400

        category = db.session.get(Category, id)
        if not category:
            return jsonify({"error": "Not Found", "message": "Category not found"}), 404

        new_data = CategoryBase.model_validate(raw_data)
        category.name = new_data.name

        db.session.commit()
        db.session.refresh(category)

        return jsonify(CategoryBase.model_validate(category).model_dump()), 200

    except ValidationError as exc:
        return jsonify({"error": "Validation Error", "message": exc.errors()}), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": str(exc)}), 400


@categories_bp.route('/<int:id>', methods=["DELETE"])
def delete_category(id):
    category = db.session.get(Category, id)
    if not category:
        return jsonify({"error": "Not Found", "message": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Category {id} deleted successfully"}), 200