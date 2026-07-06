import re
from difflib import SequenceMatcher                                       #Compare two strings and return a similarity ratio.

#Compares two strings and how similar they are.
def similarity(a, b):                                                            
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()

#Cleans and normalizes the skill text.
def normalize_skill(skill):                                                     

    skill = skill.lower().strip()
    skill = skill.replace("-", " ")
    skill = skill.replace("/", " ")
    return skill

#Main function
def calculate_match_score(
    resume_text,                                                         #The candidate's resume text.
    required_skills,                                                     # list of skills that are required for the job.
    candidate_experience,                                                #years of experience the candidate has.
    required_experience                                                  #years of experience required for the job.
):

    resume_text = normalize_skill(resume_text)                          #cleans the resume_text before matching it with the required skills.

    matched_skills = []

    missing_skills = []

#checks each required skill against the candidate's resume text to find matches and missing skills.
    for skill in required_skills:

        skill = normalize_skill(skill)

        pattern = r'\b' + re.escape(skill) + r'\b'                    #creates a regex pattern to match the skill as a whole word in the resume text.

        if re.search(pattern, resume_text):                           #checks if the exact skill exists in the resume.
            matched_skills.append(skill)

        else:
            found = False
            words = resume_text.split()                            #split resume into words

            for word in words:                                     #if similarity greaterthan 85%, consider at a match and stops checking further for that skill.
                if similarity(skill, word) > 0.85:                 
                    matched_skills.append(skill)
                    found = True
                    break
            if not found:                                        #if no match found then add the skill to the missing_skills list.
                missing_skills.append(skill)

    # Removes duplicates
    matched_skills = list(set(matched_skills))

    missing_skills = list(set(missing_skills))

    # skills contribute upto 80% of the total score.
    if len(required_skills) > 0:

        skill_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 80

    else:

        skill_score = 0

    # Experience contributes upto 20% of the total score.
    if candidate_experience >= required_experience:

        experience_score = 20

    else:

        experience_score = 0

    # Total score.
    total_score = skill_score + experience_score
    return {

        "score": round(total_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }