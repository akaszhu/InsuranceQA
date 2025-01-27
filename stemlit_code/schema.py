from pydantic import BaseModel,Field
import uuid
from typing import List, Optional,Dict
from datetime import date, datetime, time, timedelta

class TestCase(BaseModel):
    test_case_id: int
    test_case_description: str
    module: str
    expected_output: str
    steps_to_achieve: str
    success_criteria: str

class TestCaseCreateRequest(BaseModel):
    company_details: dict
    project_details: dict
    test_cases: list[TestCase]
class Scope(BaseModel):
    scope_topic:str
    description:str

class StakeHolders(BaseModel):
    title:str
    description:str
class Requirements(BaseModel):
    requirement: str

class Freatures(BaseModel):
    freatures: str
class Module(BaseModel):
    module_name:str
    requirements:list[Requirements]
    feature:list[Freatures]
class ProjectDetails(BaseModel):
    project_details: str = Field(..., description="Overview of the project")
    scopes: list[Scope] = Field(default_factory=dict, description="Project scopes")
    stakeholders: list[StakeHolders] = Field(default_factory=dict, description="Project stakeholders")
    modules: list[Module] = Field(default_factory=list, description="Project modules")

class Story(BaseModel):
    story_id: str = Field(default_factory=uuid.uuid4, description="Unique identifier for the story")
    story_title:str
    story_description:str
    assigned_to:str
    expected_closing_date:str
    priority:str

class UserStoryCollection(BaseModel):
    module_name:str
    phase:str
    total_days_to_close_spirint:int
    story_details:list[Story]

class UserStoryModel(BaseModel):
    """
    Comprehensive Pydantic model for a user story
    """
    id: str = Field(
        default_factory=lambda: f"US-{str(uuid.uuid4())[:8].upper()}",
        description="Unique identifier for the user story"
    )
    
    title: str = Field(
        ..., 
        description="Short, descriptive title of the user story"
    )
    
    user_role: str = Field(
        ..., 
       
        description="The user role or persona"
    )
    
    feature: str = Field(
        ..., 
       
        description="The specific feature or action"
    )
    
    business_value: str = Field(
        ..., 

        description="The business value or benefit"
    )
    
    priority: str = Field(
       
        
        description="Priority of the user story"
    )
    
    acceptance_criteria: List[str] = Field(
        ..., 
 
        description="List of acceptance criteria"
    )
    
    notes: Optional[str] = Field(

        description="Additional notes or context"
    )
    
    
    
    @property
    def full_user_story(self) -> str:
        """
        Generate the full user story statement
        """
        return f"As a {self.user_role}, I want to {self.feature} so that {self.business_value}"
    
    def to_dict(self) -> dict:
        """
        Convert the model to a dictionary
        """
        return self.to_dict()
    
    def to_json(self) -> str:
        """
        Convert the model to a JSON string
        """
        return self.to_json(indent=2)
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a UserStoryModel from a dictionary
        """
        return cls(**data)

class UserStoryCollection_old(BaseModel):
    """
    A collection of user stories
    """
    project_name: Optional[str] = Field(
        None, 
        description="Name of the project"
    )
    
    user_stories: List[UserStoryModel] = Field(
        default_factory=list,
        description="List of user stories"
    )
    
    def add_user_story(self, user_story: UserStoryModel):
        """
        Add a user story to the collection
        """
        self.user_stories.append(user_story)
    
    def get_high_priority_stories(self) -> List[UserStoryModel]:
        """
        Retrieve high-priority user stories
        """
        return [story for story in self.user_stories if story.priority == "High"]
    
    def export_to_json(self, filename: Optional[str] = None) -> str:
        """
        Export the collection to JSON
        
        :param filename: Optional file to save the JSON
        :return: JSON string representation
        """
        json_output = self.to_json(indent=2)
        
        if filename:
            with open(filename, 'w') as f:
                f.write(json_output)
        
        return json_output


class Steps(BaseModel):
    steps:str


class TestCase(BaseModel):
    test_case_id: str = Field(..., description="A unique identifier for the test case.")
    title: str = Field(..., description="A short, descriptive title for the test case.")
    preconditions: Optional[str] = Field(None, description="Any setup or prerequisites needed before running the test.")
    steps_to_execute: List[Steps] = Field(..., description="A clear sequence of actions to perform the test.")
    expected_result: str = Field(..., description="The expected behavior or output after executing the test.")
    postconditions: Optional[str] = Field(None, description="Actions to restore the environment after the test.")
    actor:str
class TestCaseResponse(BaseModel):
    module_name: str = Field(..., description="The name of the module for which test cases are generated.")
    project_name: Optional[str] = Field(None, description="The name of the project for context.")
    test_cases: List[TestCase] = Field(..., description="A list of structured test cases for the given module.")