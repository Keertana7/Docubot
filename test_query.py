from backend.query_engine import answer_query

print("DocuBot Ready! Ask anything (type 'q' to quit).")

while True:
    query = input("\nEnter your question: ")
    if query.lower() == 'q':
        break

    level = input("Choose level (Beginner / Intermediate / Expert): ").capitalize()
    answer = answer_query(query, level)
    print(f"\n=== {level} ===\n{answer}")
