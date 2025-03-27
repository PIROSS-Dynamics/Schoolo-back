from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.stats.models import QuizzResult, FindCountryResult, GuessWordResult
from apps.quizz.models import Quizz
from apps.users.models import User
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

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
                reRsults_data.append({
                    'quizz_title': result.quizz.title,
                    'score': result.score,
                    'total': result.total,
                    'date': result.date,
                    'subject' : result.quizz.subject
                })
            return Response(results_data)
        except QuizzResult.DoesNotExist:
            return Response({"error": "No quiz results found for this user."}, status=404)
        


class GuessWordResultView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        score = request.data.get('score')

        if user_id is None or score is None:
            return Response({"error": "user_id and score are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # Create a new GuessWordResult instance
        guess_word_result = GuessWordResult(user=user, score=score)
        guess_word_result.save()

        return Response({"message": "GuessWordResult score saved successfully"}, status=status.HTTP_201_CREATED)

class FindCountryResultView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        score = request.data.get('score')

        if user_id is None or score is None:
            return Response({"error": "user_id and score are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # Create a new FindCountryResult instance
        find_country_result = FindCountryResult(user=user, score=score)
        find_country_result.save()

        return Response({"message": "FindCountryResult score saved successfully"}, status=status.HTTP_201_CREATED)
    

class UserChallengeResultsView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')

        if user_id is None:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        # get results of user's challenges
        guess_word_results = GuessWordResult.objects.filter(user=user)
        find_country_results = FindCountryResult.objects.filter(user=user)

        results = []

        for result in guess_word_results:
            results.append({
                "challenge_type": "GuessWord",
                "score": result.score
            })

        for result in find_country_results:
            results.append({
                "challenge_type": "FindCountry",
                "score": result.score
            })

        return Response(results, status=status.HTTP_200_OK)