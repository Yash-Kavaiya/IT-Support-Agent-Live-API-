from google import genai
from google.genai.types import Content, Part
from playwright.sync_api import sync_playwright


def has_function_calls(response):
    """Check if response contains any function calls."""
    candidate = response.candidates[0]
    return any(hasattr(part, 'function_call') and part.function_call
               for part in candidate.content.parts)


def main():
    client = genai.Client()

    # ... (config setup from "Send a request to model" section) ...

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com")
        
        screen_width, screen_height = 1920, 1080
        
        # ... (initial contents setup from "Send a request to model" section) ...

        # Agent loop: iterate until model provides final answer
        for iteration in range(10):
            print(f"\nIteration {iteration + 1}\n")

            # 1. Send request to model (see "Send a request to model" section)
            response = client.models.generate_content(
                model='gemini-2.5-computer-use-preview-10-2025',
                contents=contents,
                config=generate_content_config,
            )

            contents.append(response.candidates[0].content)

            # 2. Check if done - no function calls means final answer
            if not has_function_calls(response):
                print(f"FINAL RESPONSE:\n{response.text}")
                break

            # 3. Execute actions (see "Execute the received actions" section)
            results = execute_function_calls(response, page, screen_width, screen_height)
            time.sleep(1)

            # 4. Capture state and create feedback (see "Capture the New State" section)
            contents.append(create_feedback(results, page))

        input("\nPress Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    main()
      