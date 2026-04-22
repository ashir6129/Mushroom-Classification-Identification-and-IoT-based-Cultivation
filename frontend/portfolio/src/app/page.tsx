export const dynamic = 'force-dynamic';

import { getGitHubRepos, transformReposToProjects } from "@/lib/github";
import { Footer } from "@/components/layout";
import {
  HeroSection,
  AboutSection,
  ProjectsSection,
  TechnicalSkillsSection,
  ProfessionalSkillsSection,
  OtherSkillsSection,
  ExperienceSection,
  ContactSection,
} from "@/components/sections";

export default async function Home() {
  // Fetch GitHub repos server-side
  const repos = await getGitHubRepos();
  const projects = transformReposToProjects(repos);

  return (
    <>
      <HeroSection />

      {/* All content sections - centered with consistent spacing */}
      <div className="space-y-0">
        <AboutSection />
        <ProjectsSection projects={projects} />
        <TechnicalSkillsSection />
        <ProfessionalSkillsSection />
        <OtherSkillsSection />
        <ExperienceSection />
        <ContactSection />
      </div>

      <Footer />
    </>
  );
}
