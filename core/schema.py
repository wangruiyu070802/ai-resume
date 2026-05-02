from pydantic import BaseModel


class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: list[str]


class Education(BaseModel):
    school: str
    major: str
    degree: str
    period: str
    highlights: list[str]


class Project(BaseModel):
    name: str
    description: str
    technologies: list[str]
    highlights: list[str]


class Skill(BaseModel):
    category: str
    items: list[str]


class Resume(BaseModel):
    name: str
    title: str
    contact: dict
    summary: str
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
    skills: list[Skill]
