from dotenv import load_dotenv
from semantic_router import Route,HybridRouter
from semantic_router.encoders import CohereEncoder
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex

load_dotenv()

# we could use this as a guide for our chatbot to avoid political conversations
faq = Route(
    name="faq",
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "How do I return a defective product?",
        "Can I exchange my order if I don't like it?",
        "Is there a warranty on the products?",
        "Do you provide cash on delivery?",
        "Can I cancel my order after placing it?",
        "What is the shipping time for my order?",
        "How do I know if my refund is processed?",
        "Are there any hidden charges on orders?",
        "How do I get assistance for a damaged product?",
        "What is the process for order replacement?",
        "refund policy",
        "return policy",
        "refund",
        "returns",
        "order cancellation",
        "payment methods",
        "cash"

    ],
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes that have 50% discount",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes in sale?",
        "What is the price of Puma running shoes?",
        "Show me Adidas shoes on discount",
        "List running shoes available in size 10",
        "Do you have sports shoes below Rs. 2000?",
        "I want black sneakers under Rs. 4000",
        "What are the best-selling shoes right now?",
        "Are there any offers on Reebok shoes?",
        "Show me casual shoes in size 8",
        "Do you have waterproof shoes in stock?",
        "Which shoes are on sale today?",
        "I want to buy formal leather shoes",
    ],
)

# we place both of our decisions together into single list
routes = [faq, sql]

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)
# encoder = CohereEncoder()
local_index = LocalIndex()

r1 = SemanticRouter(encoder=encoder,routes=routes,index=local_index,auto_sync="local")



if __name__ == "__main__":

    print(r1("What is your policy on defective products?").name)
    print(r1("Best Adidas shoes under Rs. 5000").name)
    print(r1("Can I cancel my order after buying it?").name)
    print(r1("Are any Puma shoes currently on sale").name)


