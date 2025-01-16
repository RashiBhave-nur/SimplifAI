import sys
import os
import load_db
import collections
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from jira_service import JiraService

class HelpDesk():
    """Create the necessary objects to create a QARetrieval chain"""
    def __init__(self, new_db=True):

        self.new_db = new_db
        self.template = self.get_template()
        self.embeddings = self.get_embeddings()
        self.llm = self.get_llm()
        self.prompt = self.get_prompt()

        if self.new_db:
            self.db = load_db.DataLoader().set_db(self.embeddings)
        else:
            self.db = load_db.DataLoader().get_db(self.embeddings)

        self.retriever = self.db.as_retriever()
        self.retrieval_qa_chain = self.get_retrieval_qa()

        self.jira_service = JiraService(
            server=os.environ.get('JIRA_SERVER'),
            username=os.environ.get('JIRA_USERNAME'),
            api_key=os.environ.get('JIRA_API_KEY')
        )

    def get_template(self):
        template = """
        Given these text extracts:
        -----
        {context}
        -----
        Please answer the following question in English:
        Question: {question}
        Helpful Answer:
        """
        return template

    def get_prompt(self) -> PromptTemplate:
        prompt = PromptTemplate(
            template=self.template,
            input_variables=["context", "question"]
        )
        return prompt

    def get_embeddings(self) -> OpenAIEmbeddings:
        embeddings = OpenAIEmbeddings()
        return embeddings

    def get_llm(self):
        llm = OpenAI()
        return llm

    def get_retrieval_qa(self):
        chain_type_kwargs = {"prompt": self.prompt}
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return qa

    def retrieval_qa_inference(self, question, verbose=True):
        query = {"query": question}
        answer = self.retrieval_qa_chain(query)
        sources = self.list_top_k_sources(answer, k=2)

        if verbose:
            print(sources)

        return answer["result"], sources

    def list_top_k_sources(self, answer, k=2):
        sources = [
            f'[{res.metadata["title"]}]({res.metadata["source"]})'
            for res in answer["source_documents"]
        ]

        if sources:
            k = min(k, len(sources))
            distinct_sources = list(zip(*collections.Counter(sources).most_common()))[0][:k]
            distinct_sources_str = "  \n- ".join(distinct_sources)

        if len(distinct_sources) == 1:
            return f"Here is the source that might be useful to you:  \n- {distinct_sources_str}"

        elif len(distinct_sources) > 1:
            return f"Here are {len(distinct_sources)} sources that might be useful to you:  \n- {distinct_sources_str}"

        else:
            return "Sorry, I couldn't find any resources to answer your question."
        
    def suggest_and_create_issues(self, context):
        """Analyze context and create relevant JIRA issues"""
        # Use the LLM to analyze the context and suggest issues
        prompt = """Based on the following context, suggest ONE potential JIRA issue that should be created.
        Format your response exactly like this:
        Summary: <issue summary>
        Description: <issue description>
        Type: Task

        Context:
        {context}
        """
        
        query = {"query": prompt.format(context=context)}
        suggestion = self.retrieval_qa_chain(query)
        
        # Parse the LLM response
        try:
            lines = suggestion['result'].strip().split('\n')
            issue_data = {}
            
            for line in lines:
                if line.startswith('Summary:'):
                    issue_data['summary'] = line.replace('Summary:', '').strip()
                elif line.startswith('Description:'):
                    issue_data['description'] = line.replace('Description:', '').strip()
                elif line.startswith('Type:'):
                    issue_data['type'] = line.replace('Type:', '').strip()
            
            # Validate we have all required fields
            if not all(k in issue_data for k in ['summary', 'description', 'type']):
                raise ValueError("Missing required issue fields in LLM response")
            
            # Create the JIRA issue
            issue = self.jira_service.create_ticket(
                project=os.environ.get('JIRA_PROJECT'),
                summary=issue_data['summary'],
                description=issue_data['description'],
                issue_type=issue_data['type']
            )
            
            return [issue]
            
        except Exception as e:
            print(f"Error creating JIRA issue: {str(e)}")
            return []