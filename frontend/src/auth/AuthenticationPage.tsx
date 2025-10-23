import { SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react";

function AuthenticationPage() {
  return (
    <>
      <div className="auth-container">
        <SignedOut>
          <SignIn routing="path" path="/sign-in" />
          <SignUp routing="path" path="/sign-up" />
        </SignedOut>
        <SignedIn>
          <div className="redirect-message">
            <p>you are already sign up</p>
          </div>
        </SignedIn>
      </div>
    </>
  );
}

export default AuthenticationPage;
