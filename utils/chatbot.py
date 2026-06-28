from disease_info import DISEASE_INFO


def get_ai_response(question, last_disease=None):
    if not question:
        return "👋 Ask me anything about your plants."
    question = question.lower().strip()
    # ---------------------------------------------------
    # Use previous diagnosis if user says "this", "it", etc.
    # ---------------------------------------------------

    if last_disease is not None:

        if any(word in question for word in ["this", "it", "last", "diagnosis"]):

            info = DISEASE_INFO.get(last_disease)

            if info:

                if "treat" in question or "cure" in question:

                    return f"""💊 Treatment

    {info["treatment"]}
    """

                elif "prevent" in question:

                    return f"""🛡 Prevention

    {info["prevention"]}
    """

                elif "symptom" in question:

                    return f"""🔍 Symptoms

    {info["symptoms"]}
    """

                else:

                    return f"""
    🌿 Last Diagnosis

    {last_disease.replace("___"," → ").replace("_"," ")}

    Description

    {info["description"]}
    """

    # Greetings
    if any(word in question for word in ["hi", "hello", "hey"]):
        return (
            "👋 Hello! I am PlantDoctor AI.\n\n"
            "Ask me about plant diseases, symptoms, treatment, prevention, or plant care."
        )

    # Search every disease
    for disease, info in DISEASE_INFO.items():

        clean_name = (
            disease.lower()
            .replace("___", " ")
            .replace("_", " ")
        )

        words = clean_name.split()

        # If most words appear in the question
        if any(word in question for word in words):

            if "symptom" in question:
                return f"🔍 Symptoms\n\n{info['symptoms']}"

            elif "treat" in question or "cure" in question:
                return f"💊 Treatment\n\n{info['treatment']}"

            elif "prevent" in question:
                return f"🛡 Prevention\n\n{info['prevention']}"

            elif "severity" in question:
                return f"⚠ Severity: {info['severity']}"

            else:
                return f"""
## 🌿 {clean_name.title()}

### 📝 Description
{info['description']}

### 🔍 Symptoms
{info['symptoms']}

### 💊 Treatment
{info['treatment']}

### 🛡 Prevention
{info['prevention']}
"""

    # General plant care
    if "water" in question:
        return "💧 Water according to soil moisture. Avoid overwatering."

    if "fertilizer" in question:
        return "🌱 Apply balanced fertilizer during the growing season."

    if "healthy" in question:
        return "🌿 Healthy plants need sunlight, balanced watering and regular monitoring."

    return (
        "🤖 I couldn't find information for that.\n\n"
        "Try asking:\n"
        "• What are the symptoms of Tomato Early Blight?\n"
        "• How do I treat Apple Scab?\n"
        "• How can I prevent Bacterial Spot?"
    )