from rest_framework.views import APIView
from rest_framework.response import Response
from apps.stats.models import QuizzResult
from apps.quizz.models import Quizz
from apps.users.models import User
from django.utils.timezone import now

class QuizzResultsView(APIView):

    def post(self, request, quizz_id):
        # Récupérer l'ID utilisateur envoyé par le front-end
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)
        
        # Vérifier que l'utilisateur existe
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        try:
            quizz = Quizz.objects.get(id=quizz_id)
        except Quizz.DoesNotExist:
            return Response({"error": "Quizz not found."}, status=404)

        score = request.data.get('score')
        if score is None:
            return Response({"error": "Score is required."}, status=400)

        # Créer le résultat avec l'utilisateur récupéré
        result = QuizzResult.objects.create(
            user=user,
            quizz=quizz,
            score=score,
            date=now(),
        )

        return Response({"message": "Résultat enregistré", "result_id": result.id})