import { Box, Typography, Button } from "@mui/material";
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { apiGet, apiPost } from "../../api";
import decodeJWT from "../../decodeJWT";
import Card from "../../components/Card";

/**
 * Listing all project applicants based on data table
 * @returns 
 */
function ProjectApplicantList() {
  const params = useParams();
  const [projectList, setProjectList] = useState([]);
  // Set professional as default as it is the minimal amount of perms
  const [userType, setUserType] = useState("professional");
  const [pCompanyId, setPCompanyId] = useState("professional");
  const [currUserId, setCurrUserId] = useState(0);
  const [update, setUpdate] = useState(false);
  const navigate = useNavigate();

  // Handle when the card is clicked
  const handleCardClick = (professionalId) => {
    navigate(`/profile/${professionalId}`);
  };

  // Handle approving an applicant
  const handleApprove = async (professionalId) => {
    try {
      const data = await apiPost("/project/company/approve", {
        professionalId: professionalId,
        projectId: params.projectId,
      });

      if (data.error) {
        throw new Error(data.error);
      }

      setUpdate((update) => !update);
    } catch (error) {
      alert("Could not approve professional: ", error);
    }
  };

  // Handle rejecting an applicant
  const handleReject = async (professionalId) => {
    try {
      const data = await apiPost("/project/company/reject", {
        professionalId: professionalId,
        projectId: params.projectId,
      });

      if (data.error) {
        throw new Error(data.error);
      }

      // Update the page
      setUpdate((update) => !update);
    } catch (error) {
      alert("Could not reject professional", error);
    }
  };

  // Check if they are the a company and the project owner
  useEffect(() => {
    const token = localStorage.getItem("token");
    const tokenData = decodeJWT(token);
    setUserType(tokenData.userType);
    setCurrUserId(tokenData.userId);

    if (tokenData.userType === "professional") {
      return;
    }

    apiGet("/project/details", `projectId=${params.projectId}`)
      .then((data) => {
        if (!data.error) {
          setPCompanyId(data.pCompanyId);
        } else {
          throw new Error("Get Project Candidate List Failed");
        }
      })
      .catch(() => {
        alert("error when getting project details");
      });
  }, [params.projectId]);

  // Get applicant list
  useEffect(() => {
    apiGet("/project/applicant/list", `projectId=${params.projectId}`)
      .then((data) => {
        if (!data.error) {
          setProjectList(data);
        } else {
          throw new Error("Get Project Candidate List Failed");
        }
      })
      .catch((error) => {
        alert("Get Project Candidate List Failed:", error);
      });
  }, [update, params.projectId]);

  return (
    userType === "company" && currUserId == pCompanyId ? (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
      >
        <Typography variant="h4" gutterBottom>
          Project Applicant List
        </Typography>
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          flexDirection="column"
          width="80vw"
          gap="10px"
        >
          {projectList
            .filter((applicant) => applicant.status == "Pending approval")
            .map((applicant) => (
              <Card
                key={applicant.professionalId}
                headerText={applicant.professionalFullName}
                descriptionOneText={applicant.professionalSkills.join(", ")}
                projectDescription={applicant.professionalEmail}
                handleClick={() => handleCardClick(applicant.professionalId)}
              >
                <Button
                  variant="contained"
                  color="error"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleReject(applicant.professionalId);
                  }}
                >
                  Reject
                </Button>
                <Button
                  variant="contained"
                  color="success"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleApprove(applicant.professionalId);
                  }}
                >
                  Approve
                </Button>
              </Card>
            ))}
        </Box>
      </Box>
    ) : (
      <Box>
        <Typography variant="p">No access allowed</Typography>
      </Box>
    )
  );
}

export default ProjectApplicantList;