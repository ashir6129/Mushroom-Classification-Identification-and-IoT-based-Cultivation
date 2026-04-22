import { getGitHubRepos, transformReposToProjects } from "@/lib/github";
import { FeaturedProjectsClient } from "./FeaturedProjectsClient";

export async function FeaturedProjects() {
    const repos = await getGitHubRepos();
    const projects = transformReposToProjects(repos);

    return <FeaturedProjectsClient projects={projects} />;
}
