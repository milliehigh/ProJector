import { Divider, Avatar, Typography, Button } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import styles from '../styles/Professional/Certificate.module.css'
import PropTypes from 'prop-types';

/**
 * 
 * @param {*} param0 
 * @returns 
 * 
 * Component for creating cards to display a professional's certificate.
 * On the card, it displays the project name and company that the professional worked for
 * There is also a download button to download the certificate
 */
const Certificates  = ({ certificates, ownProfile }) => {
  // when the download button is clicked, the certificate is downloaded
	const handleDownload = (cert) => {
		const link = document.createElement('a');
		link.href = cert.professionalCertificate; 
		link.download = `${cert.professionalCertificateProjectName} Certificate`; 
		link.click();
	};

	return (
		<>
			<div className={styles.CertificateContainer}>
				{certificates.map((cert, idx) => (
					<>
						<div className={styles.Certificate} key={idx} >
							<div className={styles.CertificateContent} key={idx}>
								<div className={styles.CertificateContentHolder} key={idx}>
									<Avatar 
										src={cert.professionalCertificateCompanyLogo} 
										key={idx}
										sx={{ width: '60px', height: '60px', ml: '10px' }}
										variant="square"
									/>
									<div className={styles.CertificateInfo}>
										<Typography variant="h5" sx={{ml:1.5}}>{cert.professionalCertificateProjectName}</Typography>
										<Typography variant="body1" sx={{ml:1.5}} color="text.secondary">{cert.professionalCertificateCompanyName}</Typography>
									</div>
								</div>
								<div>
									{ownProfile ? <Button variant="outlined" size="small" color="neutral" 
									startIcon={<DownloadIcon fontSize="inherit" />} onClick={() => handleDownload(cert)}
									sx={{cursor: 'pointer' }} >
									Download
									</Button> : <></>}
								</div>
							</div>
						</div>
						<Divider sx={{width: '98%', ml:'0px'}}></Divider>
					</>
				))}
			</div>
		</>
	)
}

Certificates.propTypes = {
	certificates: PropTypes.object,
	ownProfile: PropTypes.bool,

}

export default Certificates;
