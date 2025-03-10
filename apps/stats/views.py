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
        
        total = request.data.get('total')
        if total is None:
            return Response({"error": "Total is required."}, status=400)

        # Créer le résultat avec l'utilisateur récupéré
        result = QuizzResult.objects.create(
            user=user,
            quizz=quizz,
            score=score,
            total=total,
            date=now(),
        )

        return Response({"message": "Résultat enregistré", "result_id": result.id})
    
class UserQuizzResultsView(APIView):
    def get(self, request, user_id):
        # Récupérer les résultats de quiz associés à cet utilisateur
        try:
            results = QuizzResult.objects.filter(user_id=user_id)
            results_data = []
            for result in results:
                results_data.append({
                    'quizz_title': result.quizz.title,
                    'score': result.score,
                    'total': result.total,
                    'date': result.date,
                    'subject' : result.quizz.subject
                })
            return Response(results_data)
        except QuizzResult.DoesNotExist:
            return Response({"error": "No quiz results found for this user."}, status=404)