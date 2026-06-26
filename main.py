import asyncio

from core.orchestrator import Orchestrator


async def main():
    print("Agentic AI Multi-Step Task System")
    print("---------------------------------")

    user_request = input("Enter a complex task: ")

    orchestrator = Orchestrator()
    result = await orchestrator.run(user_request)

    print("\nFinal Output")
    print("------------")
    print(result.get("final_answer", "No final answer generated."))


if __name__ == "__main__":
    asyncio.run(main())