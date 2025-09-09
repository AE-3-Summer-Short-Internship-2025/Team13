import { createContext, useState } from "react";

export const MenuContext = createContext();

export function MenuProvider({ children }) {
    const [menu, setMenu] = useState(false);

    return (
        <MenuContext.Provider value={{ menu, setMenu }}>
            {children}
        </MenuContext.Provider>
    );
}