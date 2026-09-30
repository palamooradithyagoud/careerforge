import { PageLoader } from "@/components/common/BoxLoader";

export default function Loading() {
  return (
    <div className="min-h-screen bg-[#0C0C10] flex items-center justify-center">
      <PageLoader
        title="Loading ASCEND"
        subtitle="Retrieving intelligence profile & curated opportunities..."
        size={84}
      />
    </div>
  );
}
