
# scripts/benchmark.py
import click
import timeit
import os
from pathlib import Path
from oslolo.core.archive_manager import ArchiveManager

DUMMY_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
DUMMY_FILE_NAME = "benchmark_file.bin"

def create_dummy_file(directory: Path) -> Path:
    path = directory / DUMMY_FILE_NAME
    click.echo(f"Creating dummy file of size {DUMMY_FILE_SIZE / 1024 / 1024:.2f} MB...")
    with open(path, "wb") as f:
        f.write(os.urandom(DUMMY_FILE_SIZE))
    return path

@click.command()
@click.option('--format', 'archive_format', default='zip', type=click.Choice(['zip', '7z', 'tar']), help='Archive format to benchmark.')
@click.option('--runs', default=3, help='Number of runs for timing.')
@click.pass_context
def benchmark(ctx, archive_format, runs):
    """Runs a simple compression/decompression benchmark."""
    manager = ArchiveManager()
    
    with click.get_current_context().scope() as scope:
        temp_dir = Path("./benchmark_temp")
        temp_dir.mkdir(exist_ok=True)
        
        dummy_file = create_dummy_file(temp_dir)
        archive_path = temp_dir / f"benchmark_archive.{archive_format}"
        extract_dir = temp_dir / "extracted"
        extract_dir.mkdir(exist_ok=True)
        
        click.echo(f"\n--- Benchmarking {archive_format.upper()} ---")

        # Benchmark Creation
        create_stmt = lambda: manager.create(str(archive_path), [str(dummy_file)], format=archive_format)
        create_time = timeit.timeit(create_stmt, number=runs) / runs
        click.echo(f"  Creation Time:   {create_time:.4f} seconds (avg of {runs} runs)")

        # Benchmark Extraction
        extract_stmt = lambda: manager.extract(str(archive_path), str(extract_dir))
        extract_time = timeit.timeit(extract_stmt, number=runs) / runs
        click.echo(f"  Extraction Time: {extract_time:.4f} seconds (avg of {runs} runs)")
        
        # Cleanup
        click.echo("Cleaning up...")
        for p in temp_dir.glob("*"):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                # Simple cleanup, a real script would use shutil.rmtree
                for sub_p in p.glob("*"): sub_p.unlink()
                p.rmdir()
        temp_dir.rmdir()


if __name__ == "__main__":
    benchmark()
