import { SignedIn, UserButton, SignedOut } from "@clerk/clerk-react";
import { Link, Navigate, Outlet } from "react-router-dom";

function Layout() {
  return (
    <>
      <div className="app-layout">
        <header className="app-header">
          <div className="header-content">
            <h1>Code Challenge Generator</h1>
            <nav>
              <SignedIn>
                <Link to="/">Generate Challenge</Link>
                <Link to="/history">History</Link>
                <UserButton />
              </SignedIn>
            </nav>
          </div>
        </header>
        <main className="app-main">
          <SignedOut>
            <Navigate to="/sign-in" replace />
          </SignedOut>
          <SignedIn>
            <Outlet />
          </SignedIn>
        </main>
      </div>
    </>
  );
}

export default Layout;
