import React, { createContext, useContext, useState, ReactNode } from 'react';
import { UserData } from '../types';

interface UserContextType {
    userData: Partial<UserData>;
    updateUserData: (data: Partial<UserData>) => void;
    resetUserData: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [userData, setUserData] = useState<Partial<UserData>>({});

    const updateUserData = (data: Partial<UserData>) => {
        setUserData((prev) => ({ ...prev, ...data }));
    };

    const resetUserData = () => {
        setUserData({});
    };

    return (
        <UserContext.Provider value={{ userData, updateUserData, resetUserData }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUserData = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUserData must be used within UserProvider');
    }
    return context;
};
