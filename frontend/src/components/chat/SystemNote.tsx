import React from 'react';

interface SystemNoteProps {
    text: string;
}

const SystemNote = ({ text }: SystemNoteProps) => {
    return <div className="py-2 text-sm opacity-80 select-none">{text}</div>;
};

export default SystemNote;
