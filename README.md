
<h1>CodeTutors</h1>

<h2>Motivation</h2>
<p>The quest for quality education is universal, yet the challenge often lies in finding the right match between students and tutors. Our project, CodeTutors, seeks to revolutionize this search by leveraging technology to closely align educational support with students' specific needs and learning outcomes. Recognizing the role of tangible academic achievements in evaluating teaching effectiveness and tutors’ actual teaching abilities, we propose an innovative approach to enhance the matchmaking process on our platform. We envision a platform where students can find credible tutors that match their various requirements and where tutors can earn an income, using their skills, and eventually develop into better tutors using our unique TutorScore system.</p>

<h2>Features</h2>

<h3>Profile Creation and Management (Core)</h3>
    <ul>
        <li><strong>Creation:</strong>
            <ul>
                <li>Mechanism for both tutors and students.</li>
                <li>Sign-up through Google/Outlook/LinkedIn, or by providing an email and password (with optional verification code feature).</li>
                <li>Separate profile creation pages for tutors and students to collect respective fields of information.</li>
            </ul>
        </li>
        <li><strong>Maintenance:</strong>
            <ul>
                <li>Users can manage and update their personal information.</li>
                <li>Use of a database (PostgreSQL with Django) to store tutor and student information.</li>
            </ul>
        </li>
    </ul>

<h3>TutorScore System</h3>
<p>Each tutor will have a TutorScore, similar to the rating system on Carousell. The score is computed using the average of several metrics, implemented in the form of a questionnaire given to the students two months after starting the first lesson or upon termination of the tutoring service. Students can filter tutors by their TutorScore.</p>

<h4>Metrics</h4>
<ul>
        <li>Clarity and understandability of the tutor’s explanations.</li>
        <li>How well the tutor addresses questions and concerns.</li>
        <li>Engagement during tutoring sessions.</li>
        <li>Responsiveness to questions and concerns outside of scheduled sessions.</li>
        <li>Further criteria may be added in the future.</li>
</ul>

<h3>Filter System</h3>
<ul>
    <li><strong>Location:</strong> Use Google Maps API to locate students' houses from that of tutors for face-to-face sessions. Tutors can filter available students based on location.</li>
    <li><strong>Price:</strong> Students and tutors can filter based on price per hour.</li>
    <li><strong>Subjects:</strong> Students can filter tutors by subjects taught, and tutors can filter students by subjects they are looking for.</li>
    <li><strong>Years of Experience:</strong> Students can filter tutors by their number of years of experience.</li>
</ul>

    <h3>UI/UX</h3>
    <ul>
        <li><strong>Display:</strong>
            <ul>
                <li>Each card shows the tutor’s name and overall rating.</li>
                <li>A more details button reveals strengths, weaknesses, and past reviews.</li>
                <li>Start messaging icon allows direct messaging with the tutor.</li>
            </ul>
        </li>
    </ul>

<h3>Job Posting</h3>
<p>Students can post job postings to find a tutor specifying subject, rate, and TutorScore requirements. Tutors can see these postings on the Google Map interface and apply for the job postings.</p>

<h3>Payment System</h3>
<p>To monetize our system, tutors are required to pay to keep their profiles visible and to apply to job requests. This is achieved by integrating the Stripe API. Tutors can also pay extra for profile priority to be displayed preferentially to students.</p>

<h2>SWE Practices</h2>
    <ul>
    <li>User Testing</li>
    <li>Automated Testing (optional)</li>
    <li>Version Control</li>
    <li>Unit Testing + Integrated Testing</li>
    <li>User-Centric Designs (personalization of the app)</li>
    <li>Don’t Repeat Yourself (DRY) Principle</li>
</ul>

<h2>Milestone 1 Report</h2>
<p>Insert detailed text for Milestone 1 Report here.</p>

<h2>Installation</h2>
<p>Instructions for setting up the development environment.</p>
<ol>
    <li>Clone the repository.</li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Set up the database: <code>python manage.py migrate</code></li>
    <li>Run the server: <code>python manage.py runserver</code></li>
</ol>

    <h1>Dependencies </h1>
<div>
  <ol>
    <li>python3 for virtual env</li>
    <li>Django</li>
    <li>Sqlite</li>
    <li>npm</li>
    <li>react-dom</li>
    <li>Nextjs</li>
    <li>MaterialUI</li>
    <li>Babel</li>
    <li>Webpack</li>
  </ol>
</div>

<h2>Contributing</h2>
<p>Please read our <a href="CONTRIBUTING.md">CONTRIBUTING.md</a> for the process for submitting pull requests.</p>

<h2>Acknowledgments</h2>
<p>Thanks to everyone who has contributed to this project.</p>


