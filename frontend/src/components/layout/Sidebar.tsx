import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faComment, faClock } from '@fortawesome/free-regular-svg-icons';

const Sidebar = () => {
    return (
        <div className="bg-white w-80 p-1 items-start">
            <div className="flex items-center hover:scale-105 transition-all hover:cursor-pointer">
                <FontAwesomeIcon icon={faComment} className="m-2" />
                <p>New Chat</p>
            </div>
            <hr className="my-3" />
            <div className="flex items-center hover:scale-105 transition-all hover:cursor-pointer">
                <FontAwesomeIcon icon={faClock} className="m-2" />
                <p>History from Chat</p>
            </div>
        </div>
    );
};

export default Sidebar;
