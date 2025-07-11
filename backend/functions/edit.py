from flask import Flask, jsonify, request
from flask_cors import CORS
from database.models import Company, Professional, Projects
from flask_jwt_extended import decode_token

app = Flask(__name__)


"""
editCompany() updates the details of an existing company.

Takes in a JSON object:
{
    id: string,
    companyPassword: string,
    companyPhoneNumber: string,
    companyWebsite: string,
    companyName: string,
    companyDescription: string,
    companyLogo: string
}

Returns:
{
    "success": "Company details updated"
}
"""
@app.route('/edit/company', methods=['PUT'])
def editCompany():
    data = request.get_json()
    companyId = data.get('id')
    password = data.get('companyPassword')
    phone = data.get('companyPhoneNumber')
    website = data.get('companyWebsite')
    name = data.get('companyName')
    description = data.get('companyDescription')
    logo = data.get('companyLogo')

    company = Company.get_company_by_id(companyId=companyId)
    if not company:
        return jsonify({"error": "Company not found"}), 404
    
    company.set_company_password(password)
    company.set_company_details(name, phone, website, description, logo)

    return { "success": "Company details updated" }, 200


"""
editProfessional() updates the details of an existing professional.

Takes in a JSON object:
{
    id: string,
    professionalFullName: string,
    professionalPassword: string,
    professionalWebsite: string,
    professionalPhoneNumber: string,
    professionalDescription: string,
    professionalQualifications: list of strings,
    professionalEducation: string,
    professionalSkills: list of strings,
    professionalPhoto: string
}

Returns:
{
    "success": "Professional details updated"
}
"""
@app.route('/edit/professional', methods=['PUT'])
def editProfessional():

    data = request.get_json()
    id = data.get('id')
    name = data.get('professionalFullName')
    password = data.get('professionalPassword')
    website = data.get('professionalWebsite')
    number = data.get('professionalPhoneNumber')
    description = data.get('professionalDescription')
    qualification = data.get('professionalQualifications')
    education = data.get('professionalEducation')
    skills = data.get('professionalSkills')
    photo = data.get('professionalPhoto')


    professional = Professional.get_professional_by_id(professionalId=id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    
    professional.set_professional_details(name, website, number, description, qualification, education, skills, photo)
    professional.set_professional_password(password)

    return { "success": "Professional details updated" }, 200


"""
editProject() updates the details of an existing project.

Takes in a JSON object:
{
    projectId: string,
    ...additional project details to update...
}

Returns:
{
    "success": "Project details updated"
}
"""
@app.route('/edit/project', methods=['PUT']) #tested
def editProject():
    data = request.get_json()
    
    projectId = data.get("projectId")
    
    project = Projects.get_project_by_id(projectId)
    if project is None: 
        return jsonify({"error": "Project does not exist"}), 409
    
    project.edit_project_details(data)
    
    return jsonify({"success": "Project details updated"}), 200