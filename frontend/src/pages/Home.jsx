import { useNavigate } from 'react-router-dom';
import styles from "../styles/Home.module.css";
import SearchIcon from '@mui/icons-material/Search';
import image from '../assets/projector2.png';

/**
 * Style component for image
 */
const imgStyle = {
  position:'absolute',
  width: '20%',
  top: '53%',
};

/**
 * Home page for Projector platform.
 * 
 * @returns 
 */
function Home() {
  const navigate = useNavigate();
  return (
    <>
      <div className={styles.titleContainer}>
        <img src={image} style={imgStyle} />
        <h1 className={styles.title}>Find Your Dream Project Today!</h1>
        <div className={styles.searchBar}>
          <input 
            type="text" 
            className={styles.search}
            placeholder="Search for a Project Title or Company" 
          />
          <button className={styles.searchButton} onClick={()=>navigate('/allprojects')}>
            <SearchIcon fontSize="medium" />
          </button>
        </div>
      </div>
    </>
  );
}

export default Home;
