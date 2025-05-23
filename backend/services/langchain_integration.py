from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any, Optional

class LangChainService:
    def __init__(self, openai_api_key: Optional[str] = None):
        if openai_api_key:
            self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        else:
            self.llm = None

    async def enhance_prompt(self, original_prompt: str, style_description: Optional[str] = None) -> str:
        if not self.llm:
            return original_prompt

        messages = [
            SystemMessage(content="You are an expert prompt engineer for AI image generation. Your task is to take a user's basic prompt and enhance it to be more descriptive, evocative, and likely to produce a high-quality, detailed image. Consider adding details about composition, lighting, artistic style, and specific visual elements. If a style description is provided, incorporate it naturally."),
            HumanMessage(content=f"Original prompt: {original_prompt}" + (f"\nDesired style: {style_description}" if style_description else ""))
        ]

        try:
            response = await self.llm.ainvoke(messages)
            enhanced_prompt = response.content
            return enhanced_prompt
        except Exception as e:
            print(f"Error enhancing prompt with LangChain: {e}")
            return original_prompt

    async def generate_creative_brief(self, topic: str, target_audience: str) -> Dict[str, Any]:
        if not self.llm:
            return {"error": "LLM not configured."}

        template_str = """
        You are a creative director. Generate a creative brief for marketing visuals on the topic of '{topic}' aimed at '{target_audience}'.
        The brief should include:
        1. Key Message: A concise message to convey.
        2. Visual Concepts (3 ideas): Describe three distinct visual ideas.
        3. Example Prompts (for each concept): Provide a detailed AI image generation prompt for each visual concept.
        4. Suggested Color Palette: A few hex codes or descriptive color names.
        5. Tone & Style: e.g., Modern, Playful, Professional, Minimalist.

        Format your response as a JSON object.
        """
        prompt_template = PromptTemplate.from_template(template_str)
        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        try:
            response = await chain.ainvoke({"topic": topic, "target_audience": target_audience})
            brief_text = response.get("text", "{}")
            import json
            try:
                brief_json = json.loads(brief_text)
                return brief_json
            except json.JSONDecodeError:
                return {"error": "Failed to parse LLM response as JSON.", "raw_response": brief_text}
        except Exception as e:
            print(f"Error generating creative brief with LangChain: {e}")
            return {"error": str(e)}
