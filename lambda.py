# my current sagemaker endpoint is sagemaker-xgboost-2023-12-05-02-08-30-615
import json
import boto3

def lambda_handler(event, context):
    # Parse input data
    data = json.loads(event['body'])
    payload = ','.join([str(data[key]) for key in ['oldpeak', 'exang', 'cp', 'thalach', 'ca']])

    # invoke SageMaker endpoint
    runtime = boto3.client('sagemaker-runtime')
    print("Values given to model:", payload)
    response = runtime.invoke_endpoint(
        EndpointName='sagemaker-xgboost-2023-12-05-02-08-30-615',
        ContentType='text/csv',
        Body=payload
    )
    prediction = response['Body'].read().decode('utf-8')
    print("Prediction from SageMaker:", prediction)
    prediction_result = 1 if float(prediction) > 0.5 else 0
    # Print the prediction
    print("Prediction result:", prediction_result)
    
    # Return the prediction with CORS headers
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*', # Allows access from any origin
            'Access-Control-Allow-Headers': 'Content-Type', # Allowed headers
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET' # Allowed methods
        },
        'body': json.dumps({'prediction': prediction_result})
    }
