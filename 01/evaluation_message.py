class SomeModel:
    def predict(self, message: str) -> float:
        pass


def predict_message_mood(message: str, model: SomeModel, bad_threshold: float = 0.3,
                         good_threshold: float = 0.8) -> str:
    if (not isinstance(bad_threshold, float)) or (not isinstance(good_threshold, float)):
        raise TypeError

    if bad_threshold > good_threshold:
        raise ValueError("bad_threshold не может быть больше good_threshold")

    prediction = model.predict(message)

    if prediction < bad_threshold:
        return "неуд"
    elif prediction > good_threshold:
        return "отл"
    else:
        return "норм"
