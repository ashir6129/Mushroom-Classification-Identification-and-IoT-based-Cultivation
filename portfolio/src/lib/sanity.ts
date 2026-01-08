import { createClient } from "@sanity/client";
import imageUrlBuilder from "@sanity/image-url";
// @ts-ignore - Fixing Sanity type import issue for build
import type { SanityImageSource } from "@sanity/image-url/lib/types/types";
import { SanityProject, Project } from "@/types";

// Initialize Sanity client
export const sanityClient = createClient({
    projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "",
    dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || "production",
    apiVersion: "2024-01-01",
    useCdn: true, // Use CDN for faster reads in production
});

// Image URL builder
const builder = imageUrlBuilder(sanityClient);

export function urlFor(source: SanityImageSource) {
    return builder.image(source);
}

/**
 * Fetch all projects from Sanity CMS
 */
export async function getSanityProjects(): Promise<SanityProject[]> {
    const query = `*[_type == "project"] {
    _id,
    repoName,
    title,
    description,
    featured,
    images[] {
      asset-> {
        _ref,
        url
      }
    }
  }`;

    try {
        const projects = await sanityClient.fetch(query, {}, { next: { revalidate: 60 } });
        return projects;
    } catch (error) {
        console.error("Error fetching Sanity projects:", error);
        return [];
    }
}

/**
 * Get a single project by repo name from Sanity
 */
export async function getSanityProjectByRepoName(repoName: string): Promise<SanityProject | null> {
    const query = `*[_type == "project" && repoName == $repoName][0] {
    _id,
    repoName,
    title,
    description,
    featured,
    images[] {
      asset-> {
        _ref,
        url
      }
    }
  }`;

    try {
        const project = await sanityClient.fetch(query, { repoName }, { next: { revalidate: 60 } });
        return project;
    } catch (error) {
        console.error("Error fetching Sanity project:", error);
        return null;
    }
}

/**
 * Merge GitHub projects with Sanity CMS data
 */
export function mergeProjectsWithCMS(
    githubProjects: Project[],
    sanityProjects: SanityProject[]
): Project[] {
    const sanityMap = new Map(sanityProjects.map((p) => [p.repoName, p]));

    return githubProjects.map((project) => {
        const cmsData = sanityMap.get(project.name);

        if (cmsData) {
            return {
                ...project,
                title: cmsData.title || project.name,
                customDescription: cmsData.description,
                images: cmsData.images?.map((img) => img.asset?.url).filter(Boolean) as string[],
                featured: cmsData.featured || false,
            };
        }

        return project;
    });
}
