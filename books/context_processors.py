from .firebase_client import db
def categories_processor(request):
    docs = db.collection('categories').stream()
    cats = [{'id': doc.id, 'name': doc.to_dict().get('name')} for doc in docs]
    # Fallback categories if none exist in Firebase yet
    if not cats:
        cats = [{'id': 'Fiction', 'name': 'Fiction'}, {'id': 'Programming', 'name': 'Programming'}]
    return {'global_categories': cats, 'firebase_user': request.session.get('firebase_user')}
