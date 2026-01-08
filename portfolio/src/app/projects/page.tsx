import { Metadata } from "next";
import { getGitHubRepos, transformReposToProjects } from "@/lib/github";
import { ProjectsGrid } from "@/components/sections/ProjectsGrid";

export const metadata: Metadata = {
    title: "Projects | Muhammad Ashir Khan",
    description: "Browse all my projects synced from GitHub. Includes Flutter apps, web applications, and more.",
};

export default async function ProjectsPage() {
    const repos = await getGitHubRepos();
    const projects = transformReposToProjects(repos);

    return (
        <div className="pt-24 pb-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-16">
                    <span className="badge mb-4">All Projects</span>
                    <h1 className="heading-lg mb-4">My Work</h1>
                    <p className="body-lg max-w-2xl mx-auto">
                        Explore all my projects — automatically synced from GitHub. Filter by language,
                        search by name, or sort by popularity.
                    </p>
                </div>

                {/* Projects Grid with Filters */}
                <ProjectsGrid projects={projects} />
            </div>
        </div>
    );
}
