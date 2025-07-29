import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
from src.core.database import Base

class StatusEnum(enum.Enum):
    created = "Created"
    initialized = "Initialized"
    first_evaluation = "1st Round Evaluation"
    completed = "Evaluation Completed"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    projects = relationship("Project", back_populates="user")


class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="projects")

    simulations = relationship("Simulation", back_populates="project")


class Simulation(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    number_of_periods = Column(Integer)
    status = Column(Enum(StatusEnum), default=StatusEnum.created)
    feedback = Column(Text)

    project_id = Column(Integer, ForeignKey("projects.project_id"))
    project = relationship("Project", back_populates="simulations")

    primitives = relationship("Primitives", uselist=False, back_populates="simulation")
    population = relationship("Population", uselist=False, back_populates="simulation")
    demand_config = relationship("DemandConfiguration", uselist=False, back_populates="simulation")
    ibt_eau_potable = relationship("IBTEauPotable", uselist=False, back_populates="simulation")
    ibt_sanitation = relationship("IBTSanitation", uselist=False, back_populates="simulation")


class Primitives(Base):
    __tablename__ = "primitives"
    id = Column(Integer, primary_key=True)

    environmental_costs = Column(Float)
    social_data = Column(String)
    fiscalite = Column(String)  # Taxation

    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    simulation = relationship("Simulation", back_populates="primitives")


class CostsPotableWater(Base):
    __tablename__ = "costs_potable_water"
    id = Column(Integer, primary_key=True)

    fixed_costs = Column(Float)
    variable_costs = Column(Float)
    subscribers_number = Column(Integer)


class CostsSanitation(Base):
    __tablename__ = "costs_sanitation"
    id = Column(Integer, primary_key=True)

    fixed_costs = Column(Float)
    variable_costs = Column(Float)
    subscribers_number = Column(Integer)


class EnvironmentalCosts(Base):
    __tablename__ = "environmental_costs"
    id = Column(Integer, primary_key=True)

    fixed_costs = Column(Float)
    variable_costs = Column(Float)


class SocialCosts(Base):
    __tablename__ = "social_costs"
    id = Column(Integer, primary_key=True)

    car_threshold = Column(Float)
    par_threshold = Column(Float)
    poverty_threshold = Column(Float)
    extreme_poverty_threshold = Column(Float)


class Population(Base):
    __tablename__ = "population"
    id = Column(Integer, primary_key=True)
    root_database = Column(String)
    database_path = Column(String)
    eps = Column(Float)
    std = Column(Float)

    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    simulation = relationship("Simulation", back_populates="population")


class DemandConfiguration(Base):
    __tablename__ = "demand_configuration"
    id = Column(Integer, primary_key=True)
    a = Column(Float)
    b = Column(Float)
    c = Column(Float)
    d = Column(Float)
    e = Column(Float)
    f = Column(Float)
    g = Column(Float)

    perception_parameter = Column(Float)
    piscine = Column(Boolean)
    jardin = Column(Boolean)

    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    simulation = relationship("Simulation", back_populates="demand_config")


class IBTEauPotable(Base):
    __tablename__ = "ibt_eau_potable"
    id = Column(Integer, primary_key=True)
    abonnement = Column(String)

    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    simulation = relationship("Simulation", back_populates="ibt_eau_potable")

    blocks = relationship("BlockEauPotable", back_populates="ibt")


class BlockEauPotable(Base):
    __tablename__ = "block_eau_potable"
    id = Column(Integer, primary_key=True)
    seuil = Column(Float)
    price = Column(Float)

    ibt_id = Column(Integer, ForeignKey("ibt_eau_potable.id"))
    ibt = relationship("IBTEauPotable", back_populates="blocks")


class IBTSanitation(Base):
    __tablename__ = "ibt_sanitation"
    id = Column(Integer, primary_key=True)
    abonnement = Column(String)

    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    simulation = relationship("Simulation", back_populates="ibt_sanitation")

    blocks = relationship("BlockSanitation", back_populates="ibt")


class BlockSanitation(Base):
    __tablename__ = "block_sanitation"
    id = Column(Integer, primary_key=True)
    seuil = Column(Float)
    price = Column(Float)

    ibt_id = Column(Integer, ForeignKey("ibt_sanitation.id"))
    ibt = relationship("IBTSanitation", back_populates="blocks")
