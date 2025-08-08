from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import joblib
from .serializers import PredictionInputSerializer
from ml_model.feature_engineering import feature_engineer
from rest_framework.views import APIView

# Load model and label encoder (NOT separate preprocessor)
model = joblib.load('ml_model/model.pkl')
le_target = joblib.load('ml_model/label_encoder.pkl')

class PredictCropView(APIView):
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert input to DataFrame
        input_data = pd.DataFrame([serializer.validated_data])
        
        # Apply feature engineering
        df_fe = feature_engineer(input_data)
        
        # Convert to EXACT categorical types used in training
        df_fe['ph_category'] = pd.Categorical(
            df_fe['ph_category'], 
            categories=["Acidic", "Neutral", "Alkaline"], 
            ordered=True
        )
        df_fe['rainfall_level'] = pd.Categorical(
            df_fe['rainfall_level'], 
            categories=['Low', 'Medium', 'High', 'Very High'], 
            ordered=True
        )
        
        # Predict using the full pipeline (preprocessing + model)
        try:
            y_pred_encoded = model.predict(df_fe)
            crop_name = le_target.inverse_transform(y_pred_encoded)[0]
            return Response({'prediction': crop_name}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)