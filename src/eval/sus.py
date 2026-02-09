SUS_ITEMS = [
    "I think that I would like to use this system frequently.",
    "I found the system unnecessarily complex.",
    "I thought the system was easy to use.",
    "I think that I would need the support of a technical person to be able to use this system.",
    "I found the various functions in this system were well integrated.",
    "I thought there was too much inconsistency in this system.",
    "I would imagine that most people would learn to use this system very quickly.",
    "I found the system very cumbersome to use.",
    "I felt very confident using the system.",
    "I needed to learn a lot of things before I could get going with this system.",
]

def compute_sus_score(responses):
    adj = 0
    for idx, x in enumerate(responses, start=1):
        if idx % 2 == 1:
            adj += (x - 1)
        else:
            adj += (5 - x)
    return float(adj * 2.5)
