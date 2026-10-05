from google import genai
from google.genai import types
import pandas as pd
import json

Anamoly_Report = pd.read_csv("hospital_ed_anomaly_report.csv")

anamoly = Anamoly_Report.to_json(orient="records")  # Convert DataFrame to JSON string

summary_stats = {
    "total_anomalies": len(Anamoly_Report),
    "critical": (Anamoly_Report["priority_level"] == "Critical").sum(),
    "high": (Anamoly_Report["priority_level"] == "High").sum(),
    "medium": (Anamoly_Report["priority_level"] == "Medium").sum(),
    "low": (Anamoly_Report["priority_level"] == "Low").sum(),
    "max_excess_minutes": Anamoly_Report["excess_minutes"].max(),
    "average_excess_minutes": Anamoly_Report["excess_minutes"].mean()
}

ai_input_df = {
    "total_anomalies": int(summary_stats["total_anomalies"]),
    "critical_cases": int(summary_stats["critical"]),
    "high_cases": int(summary_stats["high"]),
    "medium_cases": int(summary_stats["medium"]),
    "low_cases": int(summary_stats["low"]),
    "maximum_excess_minutes": round(
        float(summary_stats["max_excess_minutes"]), 2
    ),
    "average_excess_minutes": round(
        float(summary_stats["average_excess_minutes"]), 2
    )
}
response_schema = {
    "type": "object",
    "properties": {
        "total_anomalies": {
            "type": "integer"
        },
        "critical_cases": {
            "type": "integer"
        },
        "high_cases": {
            "type": "integer"
        },
        "medium_cases": {
            "type": "integer"
        },
        "low_cases": {
            "type": "integer"
        },
        "maximum_excess_minutes": {
            "type": "number"
        },
        "average_excess_minutes": {
            "type": "number"
        },
        "executive_summary": {
            "type": "string"
        },
        "key_findings": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "recommended_actions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data_limitations": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        }
    }
}

ai_input = json.dumps(ai_input_df) # Convert python dict to JSON string 

api_key = "YOUR API KEY HERE"  # Replace with your actual API key

client = genai.Client(api_key=api_key)

system_prompt = """
You are a healthcare reporting assistant.
Use only the data supplied to you.
Do not invent facts or infer causes that are not supported by the data.
If the available data does not provide an answer, clearly state that it cannot be determined.
Answer questions regarding following topics:
1. anomaly counts
2. severity/priority
3. excess minutes
4. hospital/facility details
5. recommended actions
keep answers concise and focused on the data provided.
"""
report_context = f"""Hospital statistics: {ai_input}
Give answers only based on the provided data. Do not infer causes or make claims that are not supported by the data.
Here is the hospital anomaly report:
{anamoly}
Use this report to answer questions about individual hospitals.
Do not invent information that is not present in the report.
If the available data does not provide an answer, clearly state that it cannot be determined.

"""
try:
    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = report_context,
        config = types.GenerateContentConfig(
        system_instruction = system_prompt,
        response_mime_type="application/json",
        response_schema = response_schema
        ))
except Exception as e:
    print("Error generating content. Please check your API key and network connection.", e)
    exit()  

result = json.loads(response.text)
print("Executive Summary:")
print(result["executive_summary"])
print("\n")
print("Key Findings:")
for message in result["key_findings"]:
    print(message)
print("\n")
print("Recommended Actions:")
for rec in result["recommended_actions"]:
    print(rec)
print("\n")
print("Data Limitations:")
for dal in result["data_limitations"]:
    print(dal)

def validate_ai_response(result, ai_input_df):

    required_fields = [
        "total_anomalies",
        "critical_cases",
        "high_cases",
        "medium_cases",
        "low_cases",
        "maximum_excess_minutes",
        "average_excess_minutes",
        "executive_summary",
        "key_findings",
        "recommended_actions",
        "data_limitations"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:
        return {
            "status": "FAILED",
            "missing_fields": missing_fields
        }

    value_validation = {
        "total_anomalies": result["total_anomalies"] == ai_input_df["total_anomalies"],
        "critical_cases": result["critical_cases"] == ai_input_df["critical_cases"],
        "high_cases": result["high_cases"] == ai_input_df["high_cases"],
        "medium_cases": result["medium_cases"] == ai_input_df["medium_cases"],
        "low_cases": result["low_cases"] == ai_input_df["low_cases"],
        "maximum_excess_minutes": result["maximum_excess_minutes"] == ai_input_df["maximum_excess_minutes"],
        "average_excess_minutes": result["average_excess_minutes"] == ai_input_df["average_excess_minutes"]
    }

    failed_values = [
        field
        for field, status in value_validation.items()
        if not status
    ]

    if failed_values:
        return {
            "status": "FAILED",
            "value_errors": failed_values
        }

    return {
        "status": "PASSED"
    }

validation_result = validate_ai_response(result, ai_input_df)

print(validation_result)

if validation_result["status"] == "PASSED":
    with open("hospital_ai_report.json", "w") as file:
        json.dump(result, file, indent=4)

    print("AI report saved successfully.")


chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config = types.GenerateContentConfig(
        system_instruction= system_prompt
))

chat_context = f"""
Hospital statistics: {ai_input}
Give answers only based on the provided data. Do not infer causes or make claims that are not supported by the data.

Here is the hospital anomaly report:
{anamoly}
Use this report to answer questions about individual hospitals.
Do not invent information that is not present in the report.
""" 

chat.send_message(
chat_context)

while True:
    user_question = input("You: ")
    if user_question.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    
    response = chat.send_message(user_question)
    print("Assistant: " +response.text)