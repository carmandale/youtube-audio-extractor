def create_summary_report(total_videos, videos_to_process, successful_downloads, successful_conversions, primary_query, secondary_query, upload_date, duration):
    """
    Create and display a summary report of the process.
    
    :param total_videos: Total number of videos found in search
    :param videos_to_process: Number of videos selected for processing
    :param successful_downloads: Number of successful audio downloads
    :param successful_conversions: Number of successful MP3 conversions
    :param primary_query: Primary search query used
    :param secondary_query: Secondary search query used
    :param upload_date: Upload date filter used (if any)
    :param duration: Duration filter used (if any)
    """
    print("\n--- Summary Report ---")
    print(f"Primary Search Query: {primary_query}")
    if secondary_query:
        print(f"Secondary Search Query: {secondary_query}")
    if upload_date:
        print(f"Upload Date Filter: {upload_date}")
    if duration:
        print(f"Duration Filter: {duration}")
    print(f"Total videos found in search: {total_videos}")
    print(f"Videos selected for processing: {videos_to_process}")
    print(f"Successful audio downloads: {successful_downloads}")
    print(f"Successful MP3 conversions: {successful_conversions}")
    
    if videos_to_process > 0:
        download_rate = (successful_downloads / videos_to_process) * 100
        conversion_rate = (successful_conversions / videos_to_process) * 100
        print(f"Download success rate: {download_rate:.2f}%")
        print(f"Conversion success rate: {conversion_rate:.2f}%")
    
    print("----------------------")
