import Image from 'next/image';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-regular-svg-icons';

const Header = () => {
    return (
        <header className="bg-white flex fixed left-1 right-1 h-16 pl-2 pr-6 items-center mb-1 z-50">
            <Image
                src="/icons/logo.png"
                alt="#"
                height={32}
                width={32}
                className="h-12 w-12 mx-4 flex-shrink-0 hover:scale-105 transition-all hover:cursor-pointer"
            />
            <p>Chat-Helper</p>
            <div className="flex ml-auto items-center gap-2">
                <FontAwesomeIcon icon={faUser} />
                <p className="w-full whitespace-nowrap">Role: [Name of Role]</p>
                <Image
                    src="/icons/empty_profile_logo.jpg"
                    alt="#"
                    height={32}
                    width={32}
                    className="h-10 w-10 rounded-full object-cover flex-shrink-0 hover:scale-110 transition-all hover:cursor-pointer"
                />
            </div>
        </header>
    );
};

export default Header;
