"""Functions to operate the location table."""
from models.model import db
from models.model import Answer


def create_answer(user_id, location_id, year_old, year_new,
        source_url_root, land_usage, expansion, gold_standard_status,
        bbox_left_top_lat=0, bbox_left_top_lng=0, bbox_bottom_right_lat=0,
        bbox_bottom_right_lng=0, zoom_level=0):
    """
    Create an answer reported by an user with a location.

    Parameters
    ----------
    user_id : int
        Foreign key to the user table.
        (required)
    location_id : int
        Foreign key to the location table.
        (required)
    year_old: int
        The year where the satellite photo was taken from our geo sources.
        (required)
    year_new: int
        A newer photo to be compared with the one taken in year_old.
        (required)
    source_url_root : str
        URL to store the location on the map.
        (required)
    land_usage : int
        User's answer of judging if the land is a farm or has buildings.
        (check the answer table in model.py for the meaning of the values)
        (required)
    expansion : int
        User's answer of judging the construction is expanded.
        (check the answer table in model.py for the meaning of the values)
        (required)
    gold_standard_status : int
        The status of the answer quality.
        (check the answer table in model.py for the meaning of the values)
        (required)
    bbox_left_top_lat : float
        The latitude of the top-left corner of the bounding box for displaying the focus.
        (optional)
    bbox_left_top_lng : float
        The longitude of the top-left corner of the bounding box for displaying the focus.
        (optional)
    bbox_bottom_right_lat : float
        The latitude of the bottom-right corner of the bounding box for displaying the focus.
        (optional)
    bbox_bottom_right_lng : float
        The longitude of the bottom-right corner of the bounding box for displaying the focus.
        (optional)
    zoom_level : int
        The zoom level for displaying the location.
        (optional)

    Returns
    -------
    answer : Answer
        The newly created answer.

    Raises
    ------
    exception : Exception
        Type checking for land_usage, expansion, year_old, year_new, and gold_standard_status.
    """
    if not isinstance(land_usage, int):
        raise Exception("The land_usage shall be an integer")
    if not isinstance(expansion, int):
        raise Exception("The expansion shall be an integer")
    if not isinstance(gold_standard_status, int):
        raise Exception("The gold_standard_status shall be an integer")
    if not isinstance(year_old, int):
        raise Exception("The photo year shall be an integer")
    if not isinstance(year_new, int):
        raise Exception("The photo year shall be an integer")

    answer = Answer(user_id=user_id, location_id=location_id, year_old=year_old,
            year_new=year_new, source_url_root=source_url_root, land_usage=land_usage,
            expansion=expansion, gold_standard_status=gold_standard_status,
            bbox_left_top_lat=bbox_left_top_lat, bbox_left_top_lng=bbox_left_top_lng,
            bbox_bottom_right_lat=bbox_bottom_right_lat,
            bbox_bottom_right_lng=bbox_bottom_right_lng, zoom_level=zoom_level)

    db.session.add(answer)
    db.session.commit()

    return answer


def get_answer_count(user_id=None):
    """
    Get total number of answers.
    """
    if user_id is not None:
        answer_query = Answer.query.filter(Answer.user_id==user_id)
    else:        
        answer_query = Answer.query.filter()
    count = answer_query.count()
    return count


def get_gold_answer_count():
    """
    Get total number of answers, excluding gold answers.
    """
    answer_count = Answer.query.filter_by(gold_standard_status=0).count()
    return answer_count


def get_answer_by_id(answer_id):
    """
    Get an answer by the answer_id.

    Parameters
    ----------
    answer_id : int
        ID of the answer.

    Returns
    -------
    answer : Answer
        The retrieved answer object.
    """
    answer = Answer.query.filter_by(id=answer_id).first()
    return answer


def get_answers_by_user(user_id):
    """
    Get a list of answers by the user id.

    Parameters
    ----------
    user_id : int
        ID of the user.

    Returns
    -------
    answers : Answer
        The list of answers reported by the specified user.
    """
    answers = Answer.query.filter_by(user_id=user_id).all()
    return answers


def get_answers_by_location(location_id):
    """
    Get a list of answers by specified location.

    Parameters
    ----------
    location_id : int
        ID of the location.

    Returns
    -------
    answers : Answer
        The list of answers reported with the specified location.
    """
    answers = Answer.query.filter_by(location_id=location_id).all()
    return answers


def get_answers_by_user_and_location(user_id, location_id):
    """
    Get a list of answers by specified user id and location.

    Parameters
    ----------
    user_id : int
        ID of the user.
    location_id : int
        ID of the location.
    Returns
    -------
    answers : Answer
        The list of answers reported by the specified user and location.
    """
    answers = Answer.query.filter_by(user_id=user_id, location_id=location_id).all()

    return answers


def get_gold_answer_by_location(location_id):
    """
    Get the (first) gold answer specified by location id.

    Parameters
    ----------
    location_id : int
        ID of the location.
    Returns
    -------
    answers : Answer
        The gold answer.
    """
    answer = Answer.query.filter_by(gold_standard_status=0, location_id=location_id).first()
    return answer


def remove_answer(answer_id):
    """
    Remove an answer.

    Parameters
    ----------
    answer_id : int
        ID of the answer.

    Raises
    ------
    exception : Exception
        When no answer is found.
    """
    answer = get_answer_by_id(answer_id)

    if answer is None:
        raise Exception("Cannot find answer with id ", answer_id)

    db.session.delete(answer)
    db.session.commit()


def exam_gold_standard(location_id, land_usage, expansion):
    """
    Check the quality of the answer in comparison with the gold standard.

    Parameters
    ----------
    location_id : int
        ID of the location.
    land_usage : int
        User's answer of judging if the land is a farm or has buildings.
        (check the answer table in model.py for the meaning of the values)
    expansion : int
        User's answer of judging the construction is expanded.
        (check the answer table in model.py for the meaning of the values)

    Return
    ------
    int
        Result of the checking.
        0 means no gold standard exists.
        1 means passing the gold standard test.
        2 means failing the gold standard test.
    """
    # gold_standard_status 0 means that the answer is a gold standard
    gold_answer = Answer.query.filter_by(gold_standard_status=0, location_id=location_id).first()

    # If the gold answer doesn't exist
    if gold_answer is None:
        result = 0
        return result

    # If the gold answer exists, check the correctness
    if gold_answer.land_usage == land_usage and gold_answer.expansion == expansion:
        result = 1
    else:
        result = 2

    return result


def is_answer_reliable(location_id, land_usage, expansion):
    """
    Before submitting to DB, we judge if an answer reliable and set the location done if:
    1. The user passes the gold standard test
    2. Another user passes the gold standard test, and submitted the same answer as it.

    Parameters
    ----------
    location_id : int
        ID of the location.
    land_usage : int
        User's answer of judging if the land is a farm or has buildings.
        (check the answer table in model.py for the meaning of the values)
    expansion : int
        User's answer of judging the construction is expanded.
        (check the answer table in model.py for the meaning of the values)

    Return
    ------
    bool
        Result of the checking.
        True : Matches another good answer candiate.
        False : No other good answer candidates exist or match.
    """
    # If another user passed the gold standard quality test, and submitted an answer to the same location.
    good_answer_candidates = Answer.query.filter_by(gold_standard_status=1, location_id=location_id, land_usage=land_usage, expansion=expansion).all()

    # If the good answer candidate doesn't exist
    if len(good_answer_candidates) == 0:
        return False
    else:
        return True


def batch_process_answers(user_id, answers):
    """
    Process the answers returned by the front-end and write them into the database.

    Parameters
    ----------
    answers : list
        A list of answers provided by the front-end user.
        Each answer should be a dictionary with the following structure:
            {"location_id": XXX,
             "year_new": XXX,
             "year_old": XXX,
             "zoom_level": XXX,
             "bbox_bottom_right_lat": XXX,
             "bbox_bottom_right_lng": XXX,
             "bbox_left_top_lng": XXX,
             "bbox_left_top_lat": XXX,
             "land_usage": XXX,
             "source_url_root" : XXX,
             "expansion": XXX}
        The explanation of the parameters are in the answer table in the model.py file.

    Raises
    ------
    exception : Exception
        If "location_id" or "land_usage" or "expansion" not exist in the dictionary of an answer.
    exception : Exception
        When no gold standards are found.

    Returns
    ------
    bool
        True if passing the gold standard test.
    """
    if answers is None:
        raise Exception("Please provide answers.")
    if user_id is None:
        raise Exception("Please provide user id.")
    if len(answers) < 2:
        raise Exception("Not enough answers.")

    from models.model_operations.location_operations import set_location_done

    # The following explains the gold_test_pass_status:
    # - None means if the user's answer set doesn't include a gold standard test, which is not reasonable
    # - 1 means if the user passes the gold standard test
    # - 2 means if the user failed the gold standard test

    gold_test_pass_status = None
    non_gold_answer_id_list = []

    # The first parse is to check the gold standard test result.
    for idx in range(len(answers)):
        if "location_id" not in answers[idx]:
            raise Exception("Missing location_id in answer {}.".format(idx + 1))
        if "land_usage" not in answers[idx]:
            raise Exception("Missing land_usage in answer {}.".format(idx + 1))
        if "expansion" not in answers[idx]:
            raise Exception("Missing expansion in answer {}.".format(idx + 1))
        if "source_url_root" not in answers[idx]:
            raise Exception("Missing source_url_root in answer {}.".format(idx + 1))
            
        # Check every answer to see if gold standard exists
        status = exam_gold_standard(answers[idx]["location_id"], answers[idx]["land_usage"], answers[idx]["expansion"])
        if status == 0:
            non_gold_answer_id_list.append(idx)
        else:
            # This condition means a gold standard exists.
            # Assign gold_test_pass_status only once when an answer corresponding to a gold answer is found.
            if gold_test_pass_status is None:
                gold_test_pass_status = status

    # If no answer corresponding to the gold standard is found, something must be wrong.
    if gold_test_pass_status is None:
        raise Exception("The answer set is not correct.")

    # If user passes gold standard test, check if locations from the answers need to be set done_at.
    if gold_test_pass_status == 1:
        for idx in non_gold_answer_id_list:
            # Check if another good answer candidate exists and matches to mark the location done.
            result = is_answer_reliable(answers[idx]["location_id"], answers[idx]["land_usage"], answers[idx]["expansion"])
            if result == True:
                set_location_done(answers[idx]["location_id"], True)

    # Second parse to submit all the answers.
    for idx in range(len(answers)):
        try:
            create_answer(user_id, answers[idx]["location_id"],
                    answers[idx]["year_old"], answers[idx]["year_new"], answers[idx]["source_url_root"],
                    answers[idx]["land_usage"], answers[idx]["expansion"], gold_test_pass_status,
                    answers[idx]["bbox_left_top_lat"], answers[idx]["bbox_left_top_lng"],
                    answers[idx]["bbox_bottom_right_lat"], answers[idx]["bbox_bottom_right_lng"],
                    answers[idx]["zoom_level"])
        except Exception as errmsg:
            raise Exception(errmsg)
    if gold_test_pass_status == 1:
        return True
    else:
        return False
