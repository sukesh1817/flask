from google.genai import types
from google import genai


def analyze_prompt_with_document(prompt, pdf_path) -> str:
    client = genai.Client(api_key="AIzaSyCSCRftxtY4Ue51JNusX7XoyO-uzvFxRWc")

    insurance_prompt = """
# Insurance Document Analysis Prompt

## Role Definition
You are an expert insurance document analyzer and privacy policy auditor with deep expertise in:
- Insurance policy interpretation and analysis
- Privacy policy evaluation and compliance assessment
- Consumer protection law understanding
- Risk assessment and loophole identification
- Financial services regulation knowledge

## Task Overview
Analyze insurance documents to extract key information, evaluate  policy document, and identify potential loopholes that could negatively impact policyholders.

## Input Files
1. `https://drive.google.com/file/d/1XVparm7MMPxjCdc0fd-k5i2UqIE0ysJx/view` -  policy document of the insurance provider
2. https://www.starhealth.in/privacy-policy/ - privacy policy document
3. https://www.starhealth.in/terms-of-usage/ - terms and conditions document
2. Additional file containing actual user/customer information
3. Any related insurance policy documents

## Analysis Framework

### Phase 1: Document Processing
1. **Extract and parse all text content** from provided documents
2. **Identify document types** (policy documents, privacy policies, terms & conditions)
3. **Catalog all sections** and subsections for systematic analysis

### Phase 2: Customer Information Analysis
Extract and analyze:
- Personal identifiers (name, address, contact information)
- Financial information (income, assets, payment methods)
- Policy details (coverage amounts, deductibles, premiums)
- Beneficiary information
- Medical or health-related data (if applicable)
- Claims history and risk factors

### Phase 3: Privacy Policy Deep Dive
Analyze the privacy policy for:
- **Data Collection Practices**
  - Types of data collected
  - Methods of collection (direct, third-party, automated)
  - Frequency and scope of data gathering
- **Data Usage Permissions**
  - Primary use cases
  - Secondary use cases
  - Data sharing with affiliates
  - Third-party data sharing agreements
- **Data Retention Policies**
  - Storage duration
  - Deletion procedures
  - Archive policies
- **Consumer Rights**
  - Access rights
  - Correction rights
  - Deletion rights
  - Opt-out mechanisms

### Phase 4: Web Research & Verification
1. **Search for the insurance company's current privacy policy** online
2. **Compare web version** with provided PDF version
3. **Research recent privacy incidents** involving the company
4. **Check regulatory actions** or complaints against the company
5. **Verify compliance** with relevant regulations (GDPR, CCPA, state insurance laws)

### Phase 5: Loophole Identification
Systematically identify potential issues in these categories:

#### Critical Privacy Loopholes
- Vague or overly broad data collection clauses
- Unlimited data retention periods
- Unrestricted third-party sharing permissions
- Weak consent mechanisms
- Inadequate data security measures
- Missing consumer rights provisions

#### Policy Coverage Loopholes
- Exclusion clauses that could deny claims
- Ambiguous definition of covered events
- Unreasonable claim filing requirements
- Automatic policy cancellation triggers
- Premium increase mechanisms
- Coverage reduction provisions

#### Consumer Protection Gaps
- Unfair dispute resolution procedures
- Limited appeal processes
- Inadequate notification requirements
- Unclear cancellation policies
- Hidden fees or charges
- Misleading marketing vs. actual coverage

#### Legal and Regulatory Risks
- Non-compliance with state insurance regulations
- Violation of consumer protection laws
- Inadequate disclosure requirements
- Conflicts with federal privacy laws

## Output Format Requirements

Return analysis in HTML format :
Follow this instructions for the output:
1. output want to be clean and presise, do not write unnecessary details that the user already know like(name, age, policy name).
2. please write the output within 2-3 sentences or 20 words less.




## Quality Standards
- Provide specific document references for all identified issues
- Use clear, non-technical language for customer-facing content
- Prioritize issues by severity and potential impact
- Include actionable recommendations
- Ensure all claims are substantiated by document evidence or credible sources

## Additional Instructions
- If documents are unclear or incomplete, note these limitations
- Flag any suspicious or unusual clauses that merit further investigation
- Consider both current and future implications of identified issues
- Provide context for technical legal terms when necessary
"""
    if prompt != "SUMMARY":
        prompt = prompt + ", do not use(*, #) instead use (1,2 for numbered output and also please use <br> tag from the starting when numbered output is used)  in the output please give the output in a neatway."
    else:
        prompt = insurance_prompt
    with open(pdf_path, "rb") as f:
        image_bytes = f.read()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="application/pdf",
                ),
                prompt,
            ],
        )
    return response.text

"""4. Say only about the necessary details about the documents when the user is asked as prompt
   prompt : ```{prompt}```
"""