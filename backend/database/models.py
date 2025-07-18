from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import JSON
import random
from sqlalchemy.ext.mutable import MutableList

# Function to create a random id
def create_id():
    existingIds = set()
    
    existingIds.update(
        item.companyId
        for item in Company.query.with_entities(Company.companyId).all()
    )

    existingIds.update(
        item.professionalId
        for item in Professional.query.with_entities(Professional.professionalId).all()
    )
    
    existingIds.update(
        item.projectId
        for item in Projects.query.with_entities(Projects.projectId).all()
    )
    
    newId = random.randint(1, 1000000)

    while newId in existingIds:
        newId = random.randint(1, 1000000)
    
    return str(newId)

### HAVE NOT BEEN TESTED (also make the create_id return a string)
def create_admin_id():
    if db.session.query(Admin).count() == 0:
        return "1"
    else:
        return create_id()

class Company(db.Model):
    __tablename__ = "companies"
    companyId = db.Column(db.String(), primary_key=True, default=create_id)
    companyName = db.Column(db.String(), default="")
    companyEmail = db.Column(db.String(), nullable=False)
    companyPhoneNumber = db.Column(db.String(), default="")
    companyWebsite = db.Column(db.String(), default="")
    companyLogo = db.Column(db.String(), default="")
    companyPassword = db.Column(db.Text())
    companyDescription = db.Column(db.String(), default="")
    listOfProjectIds = db.Column(MutableList.as_mutable(JSON), default=list)

    def __repr__(self):
        return f"<Company {self.companyEmail}>"

    def set_company_password(self, companyPassword):
        if not companyPassword:
            return
        
        self.companyPassword = generate_password_hash(companyPassword)
        db.session.commit()

    # Sets company details
    def set_company_details(self, name, phone, website, description, logo):
        newDetails = {
            "companyName": name,
            "companyPhoneNumber": phone,
            "companyWebsite": website,
            "companyDescription": description,
            "companyLogo": logo,
        }

        for dbField, value in newDetails.items():
            if value:
                setattr(self, dbField, value)
        db.session.commit()

    def check_company_password(self, companyPassword):
        return check_password_hash(self.companyPassword, companyPassword)
    
    @classmethod
    def get_company_by_email(cls, companyEmail):
        return cls.query.filter_by(companyEmail=companyEmail).first()
    
    # Gets the company based on id
    @classmethod
    def get_company_by_id(cls, companyId):
        return cls.query.filter_by(companyId=companyId).first()

    def save_company(self):
        db.session.add(self)
        db.session.commit()

    def delete_company(self):
        db.session.delete(self)
        db.session.commit()

class Professional(db.Model):
    __tablename__ = "professionals"
    professionalId = db.Column(db.String(), primary_key=True, default=create_id)
    professionalFullName = db.Column(db.String(), default="")
    professionalPhoto = db.Column(db.String(), default="")
    professionalEmail = db.Column(db.String(), nullable=False)
    professionalWebsite = db.Column(db.String(), default="")
    professionalPhoneNumber = db.Column(db.String(), default="")
    professionalDescription = db.Column(db.String(), default="")
    professionalQualifications = db.Column(db.String(), default="")
    professionalEducation = db.Column(db.String(), default="")
    professionalSkills = db.Column(MutableList.as_mutable(JSON), default=list)
    professionalPassword = db.Column(db.Text())
    professionalPastProjects = db.Column(JSON, default=list)
    listOfProfessionalRatings = db.Column(MutableList.as_mutable(JSON), default=list)
    professionalCertificates = db.Column(MutableList.as_mutable(JSON), default=list)
    professionalNotifications = db.Column(MutableList.as_mutable(JSON), default=list)
    professionalRatings = db.Column(JSON, default=dict)

    def __repr__(self):
        return f"<Professional {self.professionalEmail}>"

    def set_professional_password(self, professionalPassword):
        if not professionalPassword:
            return
        
        self.professionalPassword = generate_password_hash(professionalPassword)
        db.session.commit()

    def check_professional_password(self, professionalPassword):
        return check_password_hash(self.professionalPassword, professionalPassword)
    
    @classmethod
    def get_professional_by_email(cls, professionalEmail):
        return cls.query.filter_by(professionalEmail=professionalEmail).first()
    
    @classmethod
    def get_professional_by_id(cls, professionalId):
        return cls.query.filter_by(professionalId=professionalId).first()
    
    def add_notification(self, professionalId, message):
        target_list = getattr(self, "professionalNotifications", None)
        notification_id = str(len(self.professionalNotifications) + 1)
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        current_time = (datetime.now() + timedelta(hours=11)).strftime("%H:%M")
        
        notification = {
            "professionalNotificationId": notification_id,
            "professionalNotificationDate": current_date,
            "professionalNotificationTime": current_time,
            "professionalNotificationMessage": message
        }
        
        # self.professionalNotifications[notification_id] = notification
        target_list.insert(0, notification)
        db.session.commit()

    def save_professional(self):
        db.session.add(self)
        db.session.commit()

    def delete_professional(self):
        db.session.delete(self)
        db.session.commit()


    #Sets all data
    def set_professional_details(self, name, website, number, description, qualification, education, skills, photo):
        newDetails = {
            "professionalFullName": name,
            "professionalWebsite": website,
            "professionalPhoneNumber": number,
            "professionalDescription": description,
            "professionalQualification": qualification,
            "professionalEducation": education,
            "professionalSkills": skills,
            "professionalPhoto": photo,   
        }

        for dbField, value in newDetails.items():
            if value:
                setattr(self, dbField, value)
        db.session.commit()

class Admin(db.Model):
    __tablename__ = "admins"
    adminId = db.Column(db.String(), primary_key=True, default=create_admin_id)
    adminEmail = db.Column(db.String(), nullable=False)
    adminPassword = db.Column(db.Text())

    def __repr__(self):
        return f"<Admin {self.adminEmail}>"

    def set_admin_password(self, adminPassword):
        if not adminPassword:
            return
        
        self.adminPassword = generate_password_hash(adminPassword)
        db.session.commit()

    def check_admin_password(self, adminPassword):
        return check_password_hash(self.adminPassword, adminPassword)
    
    @classmethod
    def get_admin_by_email(cls, adminEmail):
        return cls.query.filter_by(adminEmail=adminEmail).first()
    
    @classmethod
    def get_admin_by_id(cls, adminId):
        return cls.query.filter_by(adminId=adminId).first()
    
    def save_admin(self):
        db.session.add(self)
        db.session.commit()

    def delete_admin(self):
        db.session.delete(self)
        db.session.commit()
        
class Projects(db.Model):
    __tablename__ = 'projects'
    name = db.Column(db.String(), primary_key=True, default="projects")
    projectId = db.Column(db.String(), primary_key=True, default=create_id)
    pCompanyId = db.Column(db.String(), default="")
    projectName = db.Column(db.String(), default="")
    contactEmail = db.Column(db.String(),default="")
    professionalsWanted = db.Column(db.String(),default="")
    projectObjectives = db.Column(db.String(), default="")
    projectDescription = db.Column(db.Text(), default="")
    projectStartDate = db.Column(db.String(), default="")
    projectEndDate = db.Column(db.String(), default="")
    projectLocation = db.Column(db.String(), default="")
    projectKeyResponsibilities = db.Column(db.Text())
    projectSkills = db.Column(MutableList.as_mutable(JSON), default=list)
    projectCategories = db.Column(MutableList.as_mutable(JSON), default=list)
    projectConfidentialInformation = db.Column(db.Text(), default="")
    listOfProfessionals = db.Column(MutableList.as_mutable(JSON), default=list)
    listOfApplicants = db.Column(MutableList.as_mutable(JSON), default=list)
    projectStatus = db.Column(db.String(), default="Active")
    projectCertificate = db.Column(JSON, default=dict)
    listOfProjectRatings = db.Column(MutableList.as_mutable(JSON), default=list)
    projectRatings = db.Column(JSON, default="")
    
    @classmethod
    def get_project_by_id(cls, projectId):
        return cls.query.filter_by(projectId=projectId).first()
    
    @classmethod
    def get_company_by_id(cls, companyId):
        return Company.query.filter_by(companyId=companyId).first()
    
    @classmethod
    def get_projects_by_company_id(cls, companyId):
        return cls.query.filter_by(pCompanyId=companyId).all()
    
    @classmethod
    def get_professional_by_id(cls, professionalId):
        return Professional.query.filter_by(professionalId=professionalId).first()
    
    def create_project_details(self, companyId, projectName):
        self.pCompanyId = companyId
        self.projectName = projectName
        db.session.commit()
        
    def init_project_details_for_demo(
        self, 
        companyId=None, 
        projectName=None, 
        projectObjectives=None, 
        projectDescription=None, 
        projectCategories=None, 
        projectLocation=None, 
        projectSkills=None
    ):
        self.pCompanyId = companyId
        self.projectName = projectName or "Default Project Name"  # Set a default name if missing
        self.projectObjectives = projectObjectives or "No specific objectives"
        self.projectDescription = projectDescription or "Description not provided"
        self.projectCategories = projectCategories or []
        self.projectLocation = projectLocation or "Location unspecified"
        self.projectSkills = projectSkills or []
        db.session.commit()

    def edit_project_details(self, data):
        for field, value in data.items():
            if hasattr(self, field) and field not in ['projectId', 'pCompanyId']:
                setattr(self, field, value)
        db.session.commit()
        
    def add_to_list(self, professionalId, listType, status):
        target_list = getattr(self, listType, None)
    
        if target_list is not None and isinstance(target_list, list):
            if professionalId not in target_list:
                entry = {
                    "professionalId": professionalId,
                    "status": status
                }
                target_list.append(entry)
                db.session.commit()
                return True
        return False
    
    def remove_from_list(self, professionalId, listType):
        target_list = getattr(self, listType, None)
        
        if target_list is not None and isinstance(target_list, list):
            for applicant in target_list:
                if applicant.get('professionalId') == professionalId:
                    target_list.remove(applicant)  
                    db.session.commit() 
                    return True
        return False
    
    def set_status(self, professionalId, new_status):
        # REALLY SLOW, RECREATES THE LIST...
        updated_applicants = [
            {**applicant, "status": new_status} if applicant["professionalId"] == professionalId else applicant
            for applicant in self.listOfApplicants
        ]
        
        self.listOfApplicants = updated_applicants
        db.session.commit()
        return True
        
    def save_project(self):
        db.session.add(self)
        db.session.commit()

    def delete_project(self):
        db.session.delete(self)
        db.session.commit()
        
class Skills(db.Model):
    __tablename__ = 'skills'
    name = db.Column(db.String(), primary_key=True, default="skills")
    listOfSkills = db.Column(MutableList.as_mutable(JSON), default=list)
    
    
class Categories(db.Model):
    __tablename__ = 'categories'
    name = db.Column(db.String(), primary_key=True, default="categories")
    listOfCategories = db.Column(MutableList.as_mutable(JSON), default=list)