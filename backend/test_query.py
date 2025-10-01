from query_engine import answer_query

query = "What is Ceph OSD?"

for level in ["beginner", "intermediate", "expert"]:
    print(f"\n--- {level.capitalize()} Level ---")
    answer = answer_query(query, level=level, top_k=3)
    print("Q:", query)
    print("A:", answer)
